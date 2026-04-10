
import csv
from logging import Logger, getLogger
from datetime import datetime, timedelta
from threading import Thread, Lock, Event
from scripts import get_weekday_sources, update_sources, get_playlist, TimeEvent


class Schedule:

    def __init__(self, stream_id: int, external_id: int, remaining: float = 1800.0, logger: Logger = None):
        """
        Initialize schedule manager for a radio station.

        Sets up storage for programming blocks, playlist data, and thread synchronization
        primitives for background schedule updates.

        :param stream_id: Internal stream identifier
        :param external_id: External station identifier for database queries
        :param remaining: Buffer time in seconds before next hour for update window
        :param logger: Optional logger instance
        """
        # Station identifiers
        self.__stream_id = stream_id
        self.__external_id = external_id

        # Main schedule storage (loaded on init)
        self.sources, self.playlist, self.spots = {}, {}, []

        # Update window configuration
        self.__remaining = remaining

        # Thread management and synchronization
        self.__sources_thread = None
        self.__playlist_thread = None

        self.__lock = Lock()

        # Global stop signal
        self.__stop_event = Event()

        # Worker wake-up signals
        self.__sources_event = TimeEvent()
        self.__playlist_event = TimeEvent()

        # Logging instance
        self.__logger = logger or getLogger(self.__class__.__name__)

    @property
    def remaining(self):
        """
        Get update window buffer time.

        :return: Buffer time in seconds before next hour
        """
        with self.__lock:
            return self.__remaining

    @remaining.setter
    def remaining(self, value: float):
        """
        Set update window buffer time.

        :param value: Buffer time in seconds
        """
        with self.__lock:
            self.__remaining = value

    @property
    def external_id(self):
        """
        Get station external identifier.

        :return: External station ID
        """
        with self.__lock:
            return self.__external_id

    @external_id.setter
    def external_id(self, value: int):
        """
        Set station external identifier.

        :param value: External station ID
        """
        with self.__lock:
            self.__external_id = value

    @property
    def stream_id(self):
        """
        Get internal stream identifier.

        :return: Stream ID
        """
        with self.__lock:
            return self.__stream_id

    @stream_id.setter
    def stream_id(self, value: int):
        """
        Set internal stream identifier.

        :param value: Stream ID
        """
        with self.__lock:
            self.__stream_id = value

    @property
    def is_running(self):
        """
        Check if thread is currently running.

        :return: True if running, False otherwise
        """
        return not self.__stop_event.is_set()

    def __init_schedule(self, now: datetime = None):
        """
        Initialize station schedule by loading sources and playlist.

        Fetches programming blocks and commercial breaks for the specified time.
        Must be called before starting playback.

        :param now: Datetime to initialize schedule for, defaults to current time
        :return: True if schedule loaded successfully, False otherwise
        """
        try:
            now = now or datetime.now()

            self.__logger.info(f"Initializing schedule for {now.strftime('%Y-%m-%d %H:%M:%S')}")

            # Load data outside lock to avoid blocking
            sources = self.__load_sources(now)

            if not sources:
                self.__logger.warning("No sources found for schedule initialization")
                return False

            playlist, spots = self.__load_playlist(now)

            # Quick assignment inside lock
            self.sources, self.playlist, self.spots = sources, playlist, spots

            return True

        except Exception as e:
            self.__logger.exception(f"Failed to initialize schedule: {e}")
            return False

    # ==================================================================================================================
    # GET SCHEDULE DATA
    # ==================================================================================================================
    def get_current_block(self, now: datetime = None):
        """
        Retrieve and clear pre-loaded playlist block for the current hour.

        Removes past hour blocks and returns active items. Falls back to
        source if no playlist block is available.

        :param now: Datetime to query, defaults to current time
        :return: Tuple of (items_list, None) or (None, error_message)
        """
        try:
            now = now or datetime.now()
            hour = now.hour

            with self.__lock:

                if not self.playlist and not self.sources:
                    self.__logger.warning("Playlist and source data are empty.")
                    return None, "No data available"

                # Remove all blocks from past hours
                for key in range(hour):
                    self.playlist.pop(key, None)
                    self.sources.pop(key, None)

                # Try playlist first, fall back to source
                block_list = self.playlist.pop(hour, []) or self.sources.pop(hour, [])

                if not block_list:
                    self.__logger.warning(f"No block found for {hour}.")
                    return None, f"No block found for {hour}"

                # Filter blocks that have not ended yet
                items = [item for item in block_list if item[6] > now]

                if not items:
                    self.__logger.warning(f"No active blocks found for {hour}.")
                    return None, "No active blocks found"

                self.__logger.info(f"Found {len(items)} active blocks for {hour}.")
                return items, None

        except Exception as error:
            self.__logger.error(f"Failed to get current block: {error}")
            return None, str(error)

    def get_spots(self, start_time: str):
        """
        Retrieve spot entries matching the specified start time.

        :param start_time: Start time in "HH:MM:SS" format to filter spots
        :return: Tuple of (spots_list, None) or (None, error_message)
        """
        try:
            with self.__lock:
                if not self.spots:
                    self.__logger.warning("Spot list is empty")
                    return None, "Spot list is empty"

                spot_list = [spot for spot in self.spots if spot[1] == start_time]

                self.__logger.debug(f"Found {len(spot_list)} spot(s) for {start_time}")
                return spot_list, None

        except Exception as error:
            self.__logger.exception(f"Failed to get spots for {start_time}: {error}")
            return None, str(error)

    # ==================================================================================================================
    # SCHEDULE PROCESSING HELPERS
    # ==================================================================================================================
    @staticmethod
    def __split_prg_block(playlist: dict, target: str, source: str, time_start: datetime, time_end: datetime):
        """
        Split a PRG block into max 1hr chunks and add them to the playlist dict.

        :param playlist: Playlist dict grouped by hour (mutated in place)
        :param target: Block type identifier
        :param source: Audio source identifier
        :param time_start: Block start datetime
        :param time_end: Block end datetime
        """
        prg_start = time_start

        while prg_start < time_end:
            next_hour = (prg_start + timedelta(hours=1)).replace(minute=0, second=0)
            prg_end = min(next_hour, time_end)

            playlist.setdefault(prg_start.hour, []).append(
                (target, prg_start.strftime("%H:%M:%S"), prg_end.strftime("%H:%M:%S"),
                 source, (prg_end - prg_start).total_seconds(), prg_start, prg_end)
            )

            prg_start = prg_end

    @staticmethod
    def __handle_midnight_crossing(playlist: dict, spots: list, items: list, index: int,
                                   target: str, start, source: str, time_start: datetime, end_of_day: datetime):
        """
        Truncate a block at 23:59:59 and collect remaining SPOs if target is COR.

        :param playlist: Playlist dict grouped by hour (mutated in place)
        :param spots: Spots list (mutated in place if COR followed by SPOs)
        :param items: Full items list from database
        :param index: Current index in items loop
        :param target: Block type identifier
        :param start: Original start time from database
        :param source: Audio source identifier
        :param time_start: Block start datetime
        :param end_of_day: Datetime set to 23:59:59
        """
        duration = (end_of_day - time_start).total_seconds()

        playlist.setdefault(time_start.hour, []).append(
            (target, start.strftime("%H:%M:%S"), end_of_day.strftime("%H:%M:%S"), source, duration, time_start, end_of_day)
        )

        if target != 'COR':
            return

        # COR may be followed by SPOs, collect them before stopping
        for remaining_item in items[index + 1:]:
            r_target, r_start, r_end, r_material, r_duration, r_source, r_spot_id, _ = remaining_item

            if r_target != 'SPO':
                break

            spots.append(
                (r_target, r_start.strftime("%H:%M:%S"), r_end.strftime("%H:%M:%S"), float(r_duration), r_material, r_source, r_spot_id)
            )

    @staticmethod
    def __handle_csv_midnight_crossing(playlist: dict, spots: list, rows: list, index: int,
                                       target: str, start: str, source: str, time_start: datetime, end_of_day: datetime):
        """
        Truncate a CSV block at 23:59:59 and collect remaining SPOs if target is COR.

        :param playlist: Playlist dict grouped by hour (mutated in place)
        :param spots: Spots list (mutated in place if COR followed by SPOs)
        :param rows: Full CSV rows list
        :param index: Current index in rows loop
        :param target: Block type identifier
        :param start: Original start time string
        :param source: Audio source identifier
        :param time_start: Block start datetime
        :param end_of_day: Datetime set to 23:59:59
        """
        duration = (end_of_day - time_start).total_seconds()

        playlist.setdefault(time_start.hour, []).append(
            (target, start, end_of_day.strftime("%H:%M:%S"), source, duration, time_start, end_of_day)
        )

        if target != 'COR':
            return

        # COR may be followed by SPOs, collect them before stopping
        for row in rows[index + 1:]:
            r_target, _, r_start, r_end, _, r_duration, r_material, r_source, r_spot_id = row

            if r_target != 'SPO':
                break

            spots.append((r_target, r_start, r_end, float(r_duration), r_material, r_source, r_spot_id))

    # ==================================================================================================================
    # SOURCES PROCESSING
    # ==================================================================================================================
    def __load_sources(self, now: datetime):
        """
        Load PRG sources for the current weekday and split them into 1hr blocks.

        Sources are fetched from cache/DB first, then from external source if needed.
        Blocks crossing midnight are truncated to 23:59:59.

        :param now: Datetime to determine which day to load
        :return: Dict of PRG blocks grouped by hour, or None if no sources
        """
        try:
            # Get sources for the current weekday (from DB or cache)
            sources = get_weekday_sources(self.__stream_id, now.weekday())

            # If no sources found, try to update/fetch them from external source
            if not sources:
                sources = update_sources(self.__external_id, self.__stream_id, now.weekday(), now)

                if not sources:
                    return None

            result = {}
            base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = base_date.replace(hour=23, minute=59, second=59)

            for item in sources:
                target, start, end, source = 'PRG', item.start_time, item.end_time, item.source

                time_start = base_date.replace(hour=start.hour, minute=start.minute, second=start.second)
                time_end = base_date.replace(hour=end.hour, minute=end.minute, second=end.second)

                # Midnight crossing: truncate (spots/index unused since PRG skips COR logic)
                if time_end <= time_start:
                    self.__logger.warning(f"Midnight crossing detected, truncating: {target} {start}-{end}")
                    self.__handle_midnight_crossing(
                        result, [], sources, 0, target, start, source, time_start, end_of_day
                    )
                    break

                self.__split_prg_block(result, target, source, time_start, time_end)

            return result

        except Exception as e:
            self.__logger.error(f"Failed to load sources for {now}: {e}")
            return {}

    # ==================================================================================================================
    # PLAYLIST PROCESSING
    # ==================================================================================================================
    def __load_playlist(self, now: datetime) -> tuple:
        """
        Load and organize playlist items for a full day from database.

        Items are grouped by type:
        - SPO: stored in a flat list as-is
        - PRG: split into max 1hr blocks, stored in dict by hour
        - Others (COR, MUS, C1): stored in dict by hour without splitting

        If a midnight crossing is detected, the block is truncated to 23:59:59.
        For PRG/MUS/C1 this ends processing. For COR, remaining SPOs
        are still collected before stopping.

        :param now: Datetime to determine which day to load
        :return: Tuple of (playlist_dict, spots_list) or (None, None) if no data
        """
        try:
            items = get_playlist(self.__external_id, now)

            if not items:
                return None, None

            spots, playlist = [], {}
            base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = base_date.replace(hour=23, minute=59, second=59)

            for index, item in enumerate(items):
                # Unpack row columns from database tuple
                target, start, end, material, duration, source, spot_id, _ = item

                # SPO items go directly to spots list, no time processing needed
                if target == 'SPO':
                    spots.append(
                        (target, start.strftime("%H:%M:%S"), end.strftime("%H:%M:%S"), float(duration), material, source, spot_id)
                    )
                    continue

                # Build full datetime from time components and base date
                time_start = base_date.replace(hour=start.hour, minute=start.minute, second=start.second)
                time_end = base_date.replace(hour=end.hour, minute=end.minute, second=end.second)

                # Midnight crossing: truncate and handle based on target type
                if time_end <= time_start:
                    self.__logger.warning(f"Midnight crossing detected, truncating: {target} {start}-{end}")
                    self.__handle_midnight_crossing(
                        playlist, spots, items, index, target, start, source, time_start, end_of_day
                    )
                    break

                # Calculate actual duration from time range
                duration = (time_end - time_start).total_seconds()

                # PRG blocks: split into chunks of max 1 hour (3600s)
                if target == 'PRG':
                    self.__split_prg_block(playlist, target, source, time_start, time_end)
                    continue

                # All other targets (COR, MUS, C1): store as-is by hour
                playlist.setdefault(time_start.hour, []).append(
                    (target, start.strftime("%H:%M:%S"), end.strftime("%H:%M:%S"), source, duration, time_start, time_end)
                )

            return playlist, spots

        except Exception as e:
            self.__logger.error(f"Failed to load playlist for {now}: {e}")
            return {}, []

    # ==================================================================================================================
    # FILE PROCESSING
    # ==================================================================================================================
    def read_csv(self, file_path: str, now: datetime):
        """
        Read a CSV playlist file and organize items by type.

        :param file_path: Path to the CSV file
        :param now: Datetime to determine base date (defaults to today)
        :return: Tuple of (playlist_dict, spots_list)
        """
        playlist, spots = {}, []
        base_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = base_date.replace(hour=23, minute=59, second=59)

        # Load all rows at once so slicing works in __handle_midnight_crossing
        with open(file_path, 'r', encoding='utf-8-sig', errors='replace') as f:
            rows = list(csv.reader(f))

        for index, item in enumerate(rows):
            # Extract relevant columns from CSV row
            target, _, start, end, _, duration, material, source, spot_id = item

            # SPO items go directly to spots list, no time processing needed
            if target == 'SPO':
                spots.append((target, start, end, float(duration), material, source, spot_id))
                continue

            # Parse time strings into datetime objects using base date
            start_time = datetime.strptime(start, "%H:%M:%S").time()
            end_time = datetime.strptime(end, "%H:%M:%S").time()

            time_start = base_date.replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second)
            time_end = base_date.replace(hour=end_time.hour, minute=end_time.minute, second=end_time.second)

            # Midnight crossing: truncate and handle based on target type
            if time_end <= time_start:
                self.__logger.warning(f"Midnight crossing detected, truncating: {target} {start}-{end}")
                self.__handle_csv_midnight_crossing(
                    playlist, spots, rows, index, target, start, source, time_start, end_of_day
                )
                break

            # Calculate actual duration from time range
            duration = (time_end - time_start).total_seconds()

            # PRG blocks: split into chunks of max 1 hour (3600s)
            if target == 'PRG':
                self.__split_prg_block(playlist, target, source, time_start, time_end)
                continue

            # All other targets (COR, MUS, C1): store as-is by hour
            playlist.setdefault(time_start.hour, []).append(
                (target, start, end, source, duration, time_start, time_end)
            )

        return playlist, spots

    # ==================================================================================================================
    # WORKERS
    # ==================================================================================================================
    def start(self):
        """
        Start the scheduler and all background workers.

        Initializes schedule configuration and starts worker threads
        for playlist updates and sources synchronization.

        :return: Tuple (success: bool, error_message: str or None)
        """
        with self.__lock:
            # Check if any worker is already running
            sources_alive = self.__sources_thread is not None and self.__sources_thread.is_alive()
            playlist_alive = self.__playlist_thread is not None and self.__playlist_thread.is_alive()

            if sources_alive or playlist_alive:
                self.__logger.warning("Scheduler already running")
                return False, "Scheduler already running"

            if not self.__init_schedule():
                return False, "Failed to initialize schedule sources"

            # Reset stop signal
            self.__stop_event.clear()

            # Start sources update worker
            self.__sources_thread = Thread(target=self.__sources_update_worker, daemon=False)
            self.__sources_thread.start()

            # Start playlist update worker
            self.__playlist_thread = Thread(target=self.__playlist_update_worker, daemon=False)
            self.__playlist_thread.start()

            self.__logger.info("Scheduler started successfully")
            return True, None

    def stop(self):
        """
        Stop the scheduler and all background workers.

        Signals all worker threads to stop and waits for clean shutdown.

        :return: Tuple (success: bool, error_message: str or None)
        """
        with self.__lock:
            # Check if any worker is running
            sources_alive = self.__sources_thread is not None and self.__sources_thread.is_alive()
            playlist_alive = self.__playlist_thread is not None and self.__playlist_thread.is_alive()

            if not sources_alive and not playlist_alive:
                self.__logger.warning("Scheduler not running")
                return False, "Scheduler not running"

        # Signal workers to stop
        self.__stop_event.set()

        # Wake up workers to check stop signal
        self.__sources_event.notify()
        self.__playlist_event.notify()

        # Wait for threads to finish (outside lock to avoid deadlock)
        if self.__sources_thread is not None:
            self.__sources_thread.join()

        if self.__playlist_thread is not None:
            self.__playlist_thread.join()

        self.__logger.info("Scheduler stopped successfully")
        return True, None

    def __sources_update_worker(self):
        """
        Background worker that updates sources daily at 23:00.

        Loads sources for the next day when automatically triggered at 23:00,
        or reloads current day sources when manually triggered via event.

        :return: None
        """
        self.__logger.info("Sources update worker started")

        while self.is_running:
            self.__sources_event.wait_for(30)
            # now = datetime.now()
            # target = now.replace(hour=23, minute=0, second=0, microsecond=0)
            #
            # # Schedule for tomorrow if already past 23:00
            # if now >= target:
            #     target += timedelta(days=1)
            #
            # remaining = (target - now).total_seconds()
            #
            # # Wait until 23:00 or manual trigger
            # triggered_manually = self.__sources_event.wait_for(remaining)
            #
            # if not self.is_running:
            #     self.__logger.info("Sources update worker stopped")
            #     break
            #
            # # Manual trigger: reload current day
            # if triggered_manually:
            #     load_date = now
            #     self.__logger.info(f"Manual trigger: reloading sources for {now.date()}")
            # # Automatic trigger: load next day
            # else:
            #     load_date = now + timedelta(days=1)
            #     self.__logger.info(f"Automatic trigger: loading sources for {load_date.date()}")
            #
            # sources = self.__load_sources(load_date)
            #
            # with self.__lock:
            #     self.sources = sources
            #
            # self.__logger.info(f"Sources updated: {len(sources)} loaded")

    def reload_sources(self):
        """
        Trigger immediate sources reload for current day.

        Wakes up the sources update worker to reload sources
        without waiting for the scheduled 23:00 execution.

        :return: None
        """
        self.__logger.info("Manual sources reload requested")
        self.__sources_event.notify()

    def __playlist_update_worker(self):
        """
        Background worker that updates playlist data before the next hour.

        The worker waits until the configured update window, then loads
        playlist and spots for the next hour and updates the shared state.

        :return: None
        """
        self.__logger.info("Playlist update worker started")

        while self.is_running:
            self.__playlist_event.wait_for(30)
            # now = datetime.now()
            #
            # # Calculate the beginning of the next hour
            # next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            #
            # # Wake up N seconds before the next hour
            # target = next_hour - timedelta(seconds=self.__remaining)
            #
            # # If the target time already passed, move to the next cycle
            # if now >= target:
            #     next_hour += timedelta(hours=1)
            #     target = next_hour - timedelta(seconds=self.__remaining)
            #
            # remaining = (target - now).total_seconds()
            #
            # # Wait until scheduled time or manual trigger
            # self.__playlist_event.wait_for(remaining)
            #
            # if not self.is_running:
            #     self.__logger.info("Playlist update worker stopped")
            #     break
            #
            # # Recalculate next hour after waking up
            # now = datetime.now()
            # next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
            #
            # self.__logger.info(f"Loading playlist for next hour: {next_hour.strftime('%Y-%m-%d %H:%M')}")
            #
            # playlist, spots = self.__load_current_block(next_hour)
            #
            # with self.__lock:
            #     self.playlist = playlist
            #     self.spots = spots
            #
            # self.__logger.info(f"Playlist updated: {len(playlist)} tracks, {len(spots)} spots")

    def reload_playlist(self):
        """
        Trigger immediate playlist reload for next hour.

        Wakes up the playlist update worker to reload playlist
        and spots without waiting for the scheduled execution.

        :return: None
        """
        self.__logger.info("Manual playlist reload requested")
        self.__playlist_event.notify()
