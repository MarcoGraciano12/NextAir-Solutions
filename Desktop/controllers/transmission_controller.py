"""
Stream management for audio broadcasting.

Author: Marco Graciano
Date: March 20, 2026

Description: Stream object managing encoding, broadcasting and observer pattern.
"""

from datetime import datetime, timedelta
from logging import Logger, getLogger
from threading import Thread, Lock, Event

from numpy.ma.core import remainder

from controllers.schedule import Schedule
from scripts.observers import StreamObserver
from scripts.encoders import OGGEncoder
from scripts.broadcast import Icecast
from scripts import TimeEvent


class Transmission:
    """
    Audio stream managing encoding and broadcasting operations.
    """

    def __init__(self, stream_id: int, station_id: int, stream_name: str, external_id: int, url: str, user: str,
                 password: str, channels: int, sample_rate: int, block_size: int, bitrate: str, subjects,
                 logger: Logger = None, **kwargs):
        """
        Initialize stream instance.

        :param stream_id: Stream unique identifier
        :param station_id: Station identifier
        :param stream_name: Stream name
        :param external_id: External system identifier
        :param url: Broadcast URL
        :param user: Broadcast user
        :param password: Broadcast password
        :param channels: Audio channels
        :param sample_rate: Audio sample rate
        :param block_size: Audio block size
        :param bitrate: Audio bitrate
        :param subjects: Audio sources
        :param logger: Logger instance
        :return: None
        """
        # Stream identifiers and configuration parameters
        self.stream_id = stream_id
        self.station_id = station_id
        self.stream_name = stream_name
        self.external_id = external_id

        # Broadcast server connection settings
        self.url = url
        self.user = user
        self.password = password

        # Audio processing parameters
        self.bitrate = bitrate
        self.channels = channels
        self.block_size = block_size
        self.sample_rate = sample_rate

        # Logging instance for stream operations
        self.__logger = logger or getLogger(stream_name)

        # Audio pipeline components (initialized on start)
        self.__encoder = None
        self.__observer = None
        self.__broadcast = None

        # Thread management and synchronization primitives
        self.__stream_thread = None
        self.__stream_lock = Lock()
        self.__stop_stream = Event()

        self.__timer = TimeEvent()

        # Audio Sources
        self.__subjects = subjects
        self.__schedule = None

    def __str__(self) -> str:
        """
        String representation of the transmission.
        """
        return f"{self.stream_name} | {self.sample_rate}Hz | {self.block_size} | {self.channels}ch | {self.bitrate}"

    @property
    def is_running(self):
        """
        Check if stream is currently running.

        :return: True if running, False otherwise
        """
        return not self.__stop_stream.is_set()
    # ==================================================================================================================
    # TRANSMISSION
    # ==================================================================================================================
    def _fallback_mode(self, now: datetime, fallback, observer):
        """
        Wait until next hour using fallback audio.

        Calculates remaining time to next hour and uses fallback stream while waiting.

        :param now: Current datetime reference
        :param fallback: Fallback audio source to use
        :param observer: Observer to attach/detach
        :return: None
        """
        next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        remaining = (next_hour - now).total_seconds()

        if remaining <= 0:
            return  # Edge case: already past next hour

        if remaining > 0.1:
            self.__logger.info(f"Using fallback for {remaining:.2f}s until next hour")
            fallback.attach(observer)
            self.__timer.wait_for(remaining)
            fallback.detach(observer)
        else:
            self.__timer.wait_for(remaining)

    @staticmethod
    def _group_by_source(schedule_list: list):
        """
        Group schedule items by source changes, preserving COR blocks within their current group.

        Creates separate groups when the source field changes, allowing automatic/manual mode detection.
        COR (commercial) blocks remain attached to their preceding content group rather than starting
        a new group, maintaining the relationship between programming and its associated commercials.

        :param schedule_list: List of schedule tuples containing (target, start, end, source, ...)
        :return: List of groups, where each group is a list of schedule tuples with the same source
        """
        # Initialize grouping variables for PRG source changes
        groups, group, source = [], [], None

        # Group content by source changes (COR blocks stay with current group)
        for row in schedule_list:
            # COR blocks always belong to current group
            if row[0] == 'COR':
                group.append(row)
                continue

            # Detect source change - start new group
            if source is not None and row[3] != source:
                groups.append(group)
                group = []

            # Add row to current group and update source tracker
            group.append(row)
            source = row[3]

        # Append last group if exists
        if group:
            groups.append(group)

        return groups

    def switcher(self, subject, observer, duration, attempts: int =5, fallback=None):
        """
        Attach observer to source with retry and fallback logic, wait, then detach.

        Attempts to attach the observer to the primary source with configurable retry attempts.
        If all retries fail and a fallback source is available, recursively attempts attachment
        to the fallback source.

        :param subject: Primary input source to attach
        :param observer: Observer to attach and detach
        :param duration: Wait duration in seconds while attached
        :param attempts: Number of retry attempts for source attachment
        :param fallback: Fallback input source to use if primary fails (can be None)
        :return: None
        """
        try:
            # Attempt attachment with retries
            for attempt in range(attempts):

                if subject.attach(observer):
                    self.__timer.wait_for(duration)  # Wait for specified duration
                    subject.detach(observer)  # Detach and return elapsed time
                    return

                self.__logger.warning(f"Attach {observer} on {subject} failed (attempt {attempt + 1}/{attempts})")
                self.__timer.wait_for(0.1)  # Brief delay before retry

            # Primary source exhausted, try fallback
            if fallback:
                self.__logger.warning(f"Primary source failed after {attempts} attempts, switching to fallback")
                self.switcher(fallback, observer, duration)
            else:
                # No fallback available
                self.__logger.warning(f"All sources exhausted, no fallback available")

        except Exception as error:
            self.__logger.error(f"Exception during source switching: {error}")

    def _automatic_transition(self, items, observer, fallback, subject=None):
        """
        Execute an automatic transition for a scheduled block without interruptions.

        Processes all schedule rows (programs and commercials) sequentially in order,
        skipping any segments that have already passed. Does not support wake callbacks
        or manual interruptions.

        :param items: Schedule blocks to play (list).
        :param observer: Observer to have Icecast connection.
        :param fallback: Fallback audio input for protection.
        :param subject: Dante audio input, in case of a PRG block.
        :return: None
        """
        try:
            for item in items:

                if not self.is_running:
                    self.__logger.info(f"[automatic] Stream stopped, exiting transition")
                    return

                target, start, end, source, duration, time_start, time_end = item

                if target == 'PRG' and subject is not None:
                    self.__logger.info(f"[automatic] Processing program block at {start}")
                    duration = max((time_end - datetime.now()).total_seconds(), 0)
                    self.switcher(subject=subject, observer=observer, duration=duration, fallback=fallback)
                    continue

                if target == 'COR':
                    self.__logger.info(f"[automatic] Processing commercial block at {start}")
                    # spots = self.__schedule.get_spots(start)

                    # if spots['status']:
                    #     self._commercial_transition(spots['content'], name, observer, stream)
                    # else:
                    #     self.logger.warning(f"[automatic] No spots found for COR block at {start}, skipping")

                    continue

                # # find source in audio managers
                # manager = self.deferred.get(target, None)  # Deferred Manager
                #
                # manager = self.music.get(target, manager)  # Music Manager
                manager = None

                if manager is not None:
                    # result = manager.find_input(source)
                    #
                    # if result['status']:
                    #     input_source = result['content']
                    #     duration = input_source.audio_file.get_duration()
                    pass
                else:
                    self.__logger.warning(f"[automatic] Unsupported source: {target} - {source}")

                if subject is None:
                    duration = max((time_end - datetime.now()).total_seconds(), 0)
                    self.__logger.warning(f"[automatic] source {source} in {target} not found, using fallback for {duration:.2f}s")
                    self.switcher(subject=fallback, observer=observer, duration=duration)
                    continue

                self.__logger.info(f"[automatic] Streaming {target} for {duration:.2f}s - Source: {source}")
                self.switcher(subject=subject, observer=observer, duration=duration, fallback=fallback)

        except Exception as error:
            self.__logger.exception(f"[automatic] Error in automatic transition: {str(error)}")

        finally:
            return []

    def _transition_core(self, group, observer, channel_observer, fallback, attempts=5):
        """
        Process transition logic for a schedule group, determining automatic or manual mode.

        Checks for PRG blocks and channel availability to decide transition type. Attempts
        channel observer attachment with retries, degrading to automatic if attachment fails.

        :param group: List of schedule tuples in playback order
        :param schedule: Schedule manager object handling stream programming
        :param stream_observer: Observer receiving audio block updates
        :param stream: Stream class encapsulating connection and streaming operations
        :param name: Stream name identifier
        :param channel_observer: Observer receiving GPI updates
        :param fallback: Emergency fallback subject
        :param attempts: Number of subscription retry attempts (default: 5)
        :return: Dictionary with status (bool), message (str) indicating execution result
        """
        # Check if group contains PRG block
        prg = next((row for row in group if row[0] == 'PRG'), None)

        if prg is None:  # No PRG found - use automatic transition
            return self._automatic_transition(items=group, observer=observer, fallback=fallback)

        # Get input source or use fallback
        subject = self.__subjects.get_subject(prg[3])

        if subject is None:
            self.__logger.warning(f"Input source '{prg[3]}' not found, using fallback")
            return self._automatic_transition(items=group, observer=observer, fallback=fallback)

        # Decide transition type based on channel configuration
        if not hasattr(subject, 'gpi') or subject.gpi is None:
            return self._automatic_transition(items=group, observer=observer, fallback=fallback, subject=subject)

        # try:
        #     # Configure channel observer for input source
        #     channel_observer.set_channels({input_source.dante_input.input_channel})
        #     channel_observer.set_callback(stream.wake)
        #
        #     # Attempt attachment with retries
        #     for attempt in range(attempts):
        #         attach_result = self.device_subject.attach(channel_observer)
        #
        #         if attach_result['status']:
        #             return self._manual_transition(group, schedule, stream_observer, stream, name, input_source)
        #
        #         time.sleep(0.1)  # Brief delay before retry
        #
        #     # All attach attempts failed, degrade to automatic
        #     self.logger.warning(
        #         f"[{name}] Failed to attach after {attempts} attempts, degrading to automatic transition.")
        #     self._automatic_transition(group, schedule, stream_observer, stream, name, fallback, input_source)
        #     return {'status': True, 'message': ''}
        # except Exception as error:
        #     self.logger.exception(f"[{name}] Error in transition_core: {error}.")
        #     return {'status': False, 'message': f'Error in transition: {error}.'}
        # finally:
        #     # Ensure channel observer is always detached
        #     self.device_subject.detach(channel_observer)


    def __loop(self, fallback_name: str = 'TRIONC1'):
        """
        Main streaming loop.

        :return: True if completed successfully, False on error
        """
        # Create observer to monitor this stream's lifecycle
        observer = StreamObserver(self.stream_name)

        # Retrieve the fallback subject by name
        fallback = self.__subjects.get_subject(fallback_name)

        if not fallback:
            self.__logger.info(f"Fallback '{fallback_name}' not found")
            return False

        try:
            # Set up OGG/Opus encoder with the stream's audio parameters
            encoder = OGGEncoder(
                self.stream_name, self.channels, self.sample_rate, self.block_size, self.bitrate, logger=self.__logger
            )

            observer.encoder = encoder

            # Set up Icecast broadcast connection with stream metadata
            broadcast = Icecast(
                self.stream_name, self.url, self.user, self.password, logger=self.__logger, **{
                    "Ice-Name": f"{self.stream_name} Stream",
                   "Ice-Audio-Info": f"samplerate={encoder.sample_rate};"
                                     f"bitrate={encoder.bitrate};"
                                     f"channels={encoder.channels}",
                   "Ice-Description": "Streaming by Grupo Fórmula"
                   }
            )

            observer.broadcast = broadcast

            # Abort if observer fails to start
            if not observer.start():
                self.__logger.info(f"Transmission '{self.stream_name}' could not start: observer failed")
                # return False

            # Track the last hour processed to detect hour transitions
            last_processed_hour = None

            while self.is_running:

                now = datetime.now()

                # Check if hour already processed
                if last_processed_hour == now.hour:
                    self.__logger.warning(f"Hour {now.hour} already processed, waiting for next hour")
                    self._fallback_mode(now, fallback, observer)
                    continue

                # Get current programming block for this hour
                block, msg = self.__schedule.get_current_block(now)

                if not block:
                    self.__logger.warning(f"Failed to get current block: {msg}")
                    self._fallback_mode(now, fallback, observer)
                    continue

                groups = self._group_by_source(block)

                # Buffer to hold items not played in the previous iteration
                remaining_cors = []

                # Process each group - determine manual or automatic transition
                for i, group in enumerate(groups):

                    if remaining_cors:
                        self.__logger.info(f"COR's remaining after group {i}: {len(remaining_cors)}")
                        group = remaining_cors + group

                    # Collect any COR blocks that couldn't be processed
                    remaining_cors = self._transition_core(group, observer, None, fallback)

                if remaining_cors:
                    self.__logger.warning(f"{len(remaining_cors)} COR's left unprocessed after all groups")

                # Mark current hour as processed
                last_processed_hour = now.hour

        except Exception as e:
            self.__logger.exception(f"Stream loop error: {e}")
            return False

        finally:
            observer.stop()
            self.__schedule.stop()

            self.__logger.info("Transmission stopped")

        return True

    def start(self):
        """
        Start audio streaming to broadcast server.

        :return: tuple
        """
        with self.__stream_lock:
            # Check if stream is already active
            if self.__stream_thread is not None and self.__stream_thread.is_alive():
                self.__logger.warning("Stream already running")
                return False, "Stream already running"

            self.__schedule = Schedule(self.stream_id, self.external_id, logger=self.__logger)

            success, msg = self.__schedule.start()

            if not success:
                return False, msg

            # Reset stop signal and create new thread
            self.__stop_stream.clear()
            self.__stream_thread = Thread(target=self.__loop, daemon=False)
            self.__stream_thread.start()

            self.__logger.info("Stream started successfully")
            return True, None

    def stop(self):
        """
        Stop audio streaming gracefully.

        :return: Tuple
        """
        with self.__stream_lock:
            # Check if stream is running
            if self.__stream_thread is None or not self.__stream_thread.is_alive():
                self.__logger.warning("Stream not running")
                return False, "Stream not running"

            # Signal thread to stop
            self.__stop_stream.set()

        # Wait for thread to finish (outside lock to avoid deadlock)
        self.__stream_thread.join()
        self.__logger.info("Stream stopped Successfully")
        return True, None


class TransmissionController:

    def __init__(self, subjects, logger: Logger = None):
        """
        Initialize station controller.

        :param subjects: Controller instance for managing subjects
        :param logger: Logger instance
        :return: None
        """
        self.__lock = Lock()
        self.__transmissions = {}
        self.__subjects = subjects
        self.__logger = logger or getLogger(self.__class__.__name__)

    def start_transmission(self, stream_name: str, **kwargs):
        """
        Start a stream transmission.

        :param stream_name: Stream identifier
        :param kwargs: Transmission parameters
        :return: Tuple (success: bool, result or error message)
        """
        with self.__lock:
            transmission = self.__transmissions.get(stream_name, None)

        if not transmission:
            self.__logger.info(f"{stream_name} transmission, not found, build new transmission")
            transmission = Transmission(stream_name=stream_name, subjects=self.__subjects, **kwargs)

        with self.__lock:
            if stream_name not in self.__transmissions:
                self.__transmissions[stream_name] = transmission
                self.__logger.info(f"{stream_name} added to transmissions")
            else:
                transmission = self.__transmissions[stream_name]
                self.__logger.info(f"{stream_name} already in transmissions (added by another thread)")

        return transmission.start()

    def stop_transmission(self, stream_name: str):
        """
        Stop a stream transmission.

        :param stream_name: Stream identifier
        :return: Tuple (success: bool, result or error message)
        """
        with self.__lock:
            transmission = self.__transmissions.get(stream_name, None)

        if not transmission:
            self.__logger.warning(f"Can't stop {stream_name}, transmission not found in current transmissions")
            return False, f"{stream_name} not found in transmissions"

        return transmission.stop()
