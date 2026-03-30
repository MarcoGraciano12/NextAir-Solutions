"""
Main application entry point.

Author: Marco
Date: 2025-03-25
"""

import sys
from msilib import RadioButtonGroup

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFormLayout, QWidget, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem,
    QHBoxLayout, QMessageBox, QComboBox, QDialog, QDialogButtonBox, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QAction
from resources.view import Ui_MainWindow
from qt_material import apply_stylesheet
from logging import Logger, getLogger
from passlib.hash import pbkdf2_sha256
from manager import Manager
import logging
from dialogs import AddStationDialog, AddStreamDialog


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window for testing database connection.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize main window.
        """

        super().__init__()
        self.setupUi(self)

        self.__logger = logger or getLogger(self.__class__.__name__)

        # Streaming Operations Controller
        self.__manager = Manager()

        # Setup Tables
        self.__setup_stations_table()
        self.__load_stations_table()

        self.__setup_streams_table()
        self.__load_streams_table()

        self.login_button.pressed.connect(self.login)
        self.logout_button.pressed.connect(self.logout)

        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        # ==============================================================================================================
        # STATION ACTIONS
        # ==============================================================================================================
        # Connect add station button
        self.add_station_button.pressed.connect(self.add_station)
        # Connect search button
        self.search_station_button.clicked.connect(self.search_stations)
        # Search when pressing enter the line edit
        self.search_station_line.returnPressed.connect(self.search_stations)
        # Connect refresh button to reload all stations
        self.refresh_stations_table_button.clicked.connect(self.__load_stations_table)
        # ==============================================================================================================
        # STREAMS ACTIONS
        # ==============================================================================================================
        # Connect add stream button
        self.add_stream_button.pressed.connect(self.add_stream)


    def login(self):
        self.stackedWidget.setCurrentIndex(1)

    def logout(self):
        self.stackedWidget.setCurrentIndex(0)

    def change_theme(self):
        """
        Apply new stylesheet theme to application.

        :return: None
        """
        theme = self.theme_combo.currentText()
        app = QApplication.instance()
        apply_stylesheet(app, theme=theme)

    def __confirm_deletion(self, item_name: str, item_type: str = "item") -> bool:
        """
        Show confirmation dialog for deletion action.

        Displays a Yes/No dialog asking user to confirm deletion of an item.

        :param item_name: Name of the item to delete (displayed in message)
        :param item_type: Type of item (e.g., "station", "stream", "schedule")
        :return: True if user confirmed deletion, False if cancelled
        """
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {item_type} '{item_name}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No  # Default to No for safety
        )

        return reply == QMessageBox.Yes

    @staticmethod
    def __set_centered_item(table, row: int, col: int, text: str):
        """
        Create and set a centered table item.

        :param table: QTableWidget to update
        :param row: Row index
        :param col: Column index
        :param text: Text to display
        :return: None
        """
        item = QTableWidgetItem(str(text))
        item.setTextAlignment(Qt.AlignCenter)
        table.setItem(row, col, item)

    # ==================================================================================================================
    # USERS
    # ==================================================================================================================

    # ==================================================================================================================
    # STATIONS
    # ==================================================================================================================
    def __populate_stations_combo(self, stations: list):
        """
        Populate stations combo box with station list.

        :param stations: List of Station objects
        :return: None
        """
        self.stations_combo.clear()
        for station in stations:
            # Store station_id as itemData for easy filtering
            self.stations_combo.addItem(station.station_name, station.station_id)

    def __create_station_row(self, row: int, station):
        """
        Create and populate a single station row in the table.

        Sets up table items with centered text and action buttons for
        the specified row index.

        :param row: Table row index to populate
        :param station: Station object with data to display
        :return: None
        """
        # Create centered items for all columns
        id_item = QTableWidgetItem(str(station.station_id))
        id_item.setTextAlignment(Qt.AlignCenter)

        name_item = QTableWidgetItem(str(station.station_name))
        name_item.setTextAlignment(Qt.AlignCenter)

        path_item = QTableWidgetItem(str(station.files_path))
        path_item.setTextAlignment(Qt.AlignCenter)

        self.stations_table.setItem(row, 0, id_item)
        self.stations_table.setItem(row, 1, name_item)
        self.stations_table.setItem(row, 2, path_item)

        # Create action buttons for the row
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")

        # Connect delete button with item reference
        delete_btn.clicked.connect(lambda checked, item=id_item: self.remove_station(item))

        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        self.stations_table.setCellWidget(row, 3, actions_widget)

    def __display_stations(self, stations: list):
        """
        Display a list of stations in the table.

        Clears existing rows and populates table with provided stations
        including action buttons (Edit/Delete) for each row.

        :param stations: List of Station objects to display
        :return: None
        """
        # Clear and prepare table
        self.stations_table.setRowCount(0)
        self.stations_table.setRowCount(len(stations))

        # Create each row using common method
        for i, station in enumerate(stations):
            self.__create_station_row(i, station)

    def __add_station_to_table(self, station):
        """
        Add a single station row to the table.

        Creates a new row with station data and action buttons (Edit/Delete).

        :param station: Station object to add
        :return: None
        """
        # Insert new row at the end
        row = self.stations_table.rowCount()
        self.stations_table.insertRow(row)

        # Create row using common method
        self.__create_station_row(row, station)

    def __setup_stations_table(self):
        """
        Configure the stations table widget with columns and display settings.

        Sets up column headers, disables editing, enables row selection,
        and configures column widths (ID and Actions fixed, Name/Path stretch).

        :return: None
        """
        columns = ["ID", "Name", "Path", "Actions"]

        self.stations_table.setColumnCount(len(columns))
        self.stations_table.setHorizontalHeaderLabels(columns)

        # Prevent direct cell editing - use Edit button instead
        self.stations_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Select entire row when clicking any cell
        self.stations_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Configure column widths: ID and Actions fixed, Name fixed, Path takes rest
        header = self.stations_table.horizontalHeader()

        # ID column: small fixed width for numeric values
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.stations_table.setColumnWidth(0, 60)

        # Name column: fixed width (user can resize manually)
        header.setSectionResizeMode(1, QHeaderView.Interactive)
        self.stations_table.setColumnWidth(1, 120)

        # Path column: stretches to fill all remaining space
        header.setSectionResizeMode(2, QHeaderView.Stretch)

        # Actions column: fixed width to fit Edit/Delete buttons
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.stations_table.setColumnWidth(3, 180)

        self.stations_table.verticalHeader().setDefaultSectionSize(40)

    def __load_stations_table(self):
        """
        Load and display all stations from database into the stations table widget.

        Populates the table with station data and creates action buttons (Edit/Delete)
        for each row. Clears existing rows before loading new data.

        :return: None
        """
        try:
            stations = self.__manager.get_all_stations()

            if not stations:
                self.__logger.warning("No stations found in database")
                self.statusbar.showMessage("No stations available", 3000)
                return

            # Populate combo (only if empty - first load)
            if self.stations_combo.count() == 0:
                self.__populate_stations_combo(stations)

            # Use common display method to populate table
            self.__display_stations(stations)

            self.__logger.info(f"Loaded {len(stations)} stations into table")
            self.statusbar.showMessage(f"{len(stations)} stations loaded successfully", 2000)

        except Exception as error:
            self.__logger.error(f"Failed to load stations table: {error}")
            self.statusbar.showMessage("Error loading stations. Check logs for details.", 5000)

    def search_stations(self):
        """
        Search stations by name and display matching results in table.

        Reads search term from input field and filters table to show
        only matching stations. Shows all stations if search is empty.

        :return: None
        """
        search_term = self.search_station_line.text().strip()

        # Don't search if field is empty
        if not search_term:
            self.statusbar.showMessage("Please enter a station name to search", 2000)
            return

        try:
            success, result = self.__manager.search_stations(search_term)

            if not success:
                self.__logger.warning(result)
                self.statusbar.showMessage(result, 3000)
                self.stations_table.setRowCount(0)  # Clear table
                return

            # Display search results
            stations = result
            self.__display_stations(stations)

            self.__logger.info(f"Found {len(stations)} stations matching '{search_term}'")
            self.statusbar.showMessage(f"Found {len(stations)} stations", 2000)

        except Exception as error:
            self.__logger.error(f"Error searching stations: {error}")
            self.statusbar.showMessage("Error searching stations", 5000)

    def add_station(self):
        """
        Show dialog to add a new station and save to database.

        Opens the add station dialog, validates input, creates the station
        in database, and adds it to the table if successful.

        :return: None
        """
        dialog = AddStationDialog(self, self.__logger)

        if dialog.exec() == QDialog.Accepted:
            try:
                data = dialog.get_station_data()

                # Create station in database
                success, station = self.__manager.create_station(data['name'], data['path'])

                # Check if creation failed
                if not success:
                    self.statusbar.showMessage(f"Error: {station}", 5000)
                    return

                # Add only the new row to table
                self.__add_station_to_table(station)

                # Add to combo (incremental update)
                self.stations_combo.addItem(station.station_name, station.station_id)

                self.statusbar.showMessage("Station created successfully", 2000)

            except Exception as error:
                self.__logger.error(f"Error creating station: {error}")
                self.statusbar.showMessage("Unexpected error creating station", 5000)

    def remove_station(self, id_item: QTableWidgetItem):
        """
        Remove a station from database and table UI.

        :param id_item: QTableWidgetItem reference from the ID column
        :return: None
        """
        try:
            # Get current row index from the item reference
            row = self.stations_table.row(id_item)
            station_id = int(id_item.text())
            station_name = self.stations_table.item(row, 1).text()

            # Ask for confirmation before deleting
            if not self.__confirm_deletion(station_name, "station"):
                return

            success, msg = self.__manager.delete_station(station_id)

            if not success:
                self.statusbar.showMessage(f"Error: {msg}", 5000)
                return

            # Remove row using current index (works even if previous rows were deleted)
            self.stations_table.removeRow(row)

            # Remove from combo (find and remove by station_id)
            for i in range(self.stations_combo.count()):
                if self.stations_combo.itemData(i) == station_id:
                    self.stations_combo.removeItem(i)
                    break

            self.statusbar.showMessage("Station deleted successfully", 2000)

        except Exception as error:
            self.__logger.error(f"Error removing station: {error}")
            self.statusbar.showMessage("Unexpected error deleting station", 5000)

    # ==================================================================================================================
    # STREAMS
    # ==================================================================================================================
    def __create_stream_row(self, row: int, stream):
        """
        Create and populate a single stream row in the table.

        Sets up table items with centered text and action buttons for
        the specified row index.

        :param row: Table row index to populate
        :param stream: Stream object with data to display
        :return: None
        """
        # Basic stream data
        self.__set_centered_item(self.streams_table, row, 0, stream.external_id)
        self.__set_centered_item(self.streams_table, row, 1, stream.stream_name)

        # Broadcast data or placeholders
        if not stream.broadcast:
            for col in range(2, 8):
                self.__set_centered_item(self.streams_table, row, col, "-")
        else:
            self.__set_centered_item(self.streams_table, row, 2, stream.broadcast.url)
            self.__set_centered_item(self.streams_table, row, 3, stream.broadcast.user)
            self.__set_centered_item(self.streams_table, row, 4, stream.broadcast.channels)
            self.__set_centered_item(self.streams_table, row, 5, stream.broadcast.sample_rate)
            self.__set_centered_item(self.streams_table, row, 6, stream.broadcast.block_size)
            self.__set_centered_item(self.streams_table, row, 7, stream.broadcast.bitrate)

        # Get external_id item reference for delete button
        stream_item = self.streams_table.item(row, 1)

        # Create action buttons
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")

        # Connect delete button with item reference
        delete_btn.clicked.connect(lambda checked, item=stream_item: self.remove_stream(item))

        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        self.streams_table.setCellWidget(row, 8, actions_widget)

    def __display_streams(self, streams: list):
        """
        Display a list of streams in the table.

        Clears existing rows and populates table with provided streams
        including action buttons (Edit/Delete) for each row.

        :param streams: List of Streams objects to display
        :return: None
        """
        # Clear and prepare table
        self.streams_table.setRowCount(0)
        self.streams_table.setRowCount(len(streams))

        # Create each row using common method
        for i, station in enumerate(streams):
            self.__create_stream_row(i, station)

    def __load_streams_table(self):
        """
        Load and display all streams from database into the streams table widget.

        Populates the table with stream data and creates action buttons (Edit/Delete)
        for each row. Clears existing rows before loading new data.

        :return: None
        """
        try:
            streams = self.__manager.get_all_streams()

            if not streams:
                self.__logger.warning("No streams found in database")
                self.statusbar.showMessage("No streams available", 3000)
                return

            # Use common display method to populate table
            self.__display_streams(streams)

            self.__logger.info(f"Loaded {len(streams)} streams into table")
            self.statusbar.showMessage(f"{len(streams)} streams loaded successfully", 2000)

        except Exception as error:
            self.__logger.error(f"Failed to load streams table: {error}")
            self.statusbar.showMessage("Error loading streams. Check logs for details.", 5000)

    def __add_stream_to_table(self, stream):
        """
        Add a single strean row to the table.

        Creates a new row with stream data and action buttons (Edit/Delete).

        :param stream: Stream object to add
        :return: None
        """
        # Insert new row at the end
        row = self.streams_table.rowCount()
        self.streams_table.insertRow(row)

        # Create row using common method
        self.__create_stream_row(row, stream)

    def __setup_streams_table(self):
        """
        Configure the streams table widget with columns and display settings.

        Sets up column headers, disables editing, enables row selection,
        and configures column widths (ID and Actions fixed, Name stretch).

        :return: None
        """
        columns = ["EXTERNAL ID", "NAME", "URL", "USER", "CHANNELS", "SAMPLERATE", "BLOCKSIZE", "BITRATE", "ACTIONS"]

        self.streams_table.setColumnCount(len(columns))
        self.streams_table.setHorizontalHeaderLabels(columns)

        # Prevent direct cell editing - use Edit button instead
        self.streams_table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Select entire row when clicking any cell
        self.streams_table.setSelectionBehavior(QTableWidget.SelectRows)

        # Configure column widths: ID and Actions fixed, Name fixed, Path takes rest
        header = self.streams_table.horizontalHeader()

        # EXTERNAL ID column: small fixed width for numeric values
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        self.streams_table.setColumnWidth(0, 140)

        # NAME column: small fixed width for numeric values
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # self.streams_table.setColumnWidth(0, 60)

        # URL column: small fixed width for numeric values
        header.setSectionResizeMode(2, QHeaderView.Stretch)
        # self.streams_table.setColumnWidth(0, 60)

        # USER column: small fixed width for numeric values
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.streams_table.setColumnWidth(3, 90)

        # CHANNELS column: small fixed width for numeric values
        header.setSectionResizeMode(4, QHeaderView.Fixed)
        self.streams_table.setColumnWidth(4, 120)

        # SAMPLERATE column: small fixed width for numeric values
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        self.streams_table.setColumnWidth(5, 140)

        # BLOCKSIZE column: small fixed width for numeric values
        header.setSectionResizeMode(6, QHeaderView.Fixed)
        self.streams_table.setColumnWidth(6, 120)

        # BITRATE column: small fixed width for numeric values
        header.setSectionResizeMode(7, QHeaderView.Fixed)
        self.streams_table.setColumnWidth(7, 120)

        # ACTIONS column: small fixed width for numeric values
        header.setSectionResizeMode(8, QHeaderView.Fixed)
        self.streams_table.setColumnWidth(8, 180)

        self.streams_table.verticalHeader().setDefaultSectionSize(40)

    def add_stream(self):
        """
        Show dialog to add a new stream and save to database.

        Creates stream record first, then creates associated broadcast
        configuration if stream creation succeeds.

        :return: None
        """
        # Extract station data from existing combo (reuse cached data)
        stations_data = [
            (self.stations_combo.itemData(i), self.stations_combo.itemText(i))
            for i in range(self.stations_combo.count())
        ]

        dialog = AddStreamDialog(stations_data, self, self.__logger)

        if dialog.exec() == QDialog.Accepted:
            try:
                data = dialog.get_stream_data()

                # Step 1: Create stream record
                success, stream = self.__manager.create_stream(
                    stream_name=data['name'],
                    external_id=data['external_id'],
                    station_id=data['station_id']
                )

                # Check if stream creation failed
                if not success:
                    self.statusbar.showMessage(f"Error: {stream}", 5000)
                    return

                # Step 2: Create broadcast configuration
                success, broadcast = self.__manager.create_broadcast(
                    stream_id=stream.stream_id,
                    name=data['name'],
                    url=data['url'],
                    user=data['user'],
                    password=data['password'],
                    channels=data['channels'],
                    sample_rate=data['sample_rate'],
                    block_size=data['block_size'],
                    bitrate=data['bit_rate']
                )

                # Check if broadcast creation failed
                if not success:
                    return

                # Assign broadcast to stream object (avoid DB query)
                stream.broadcast = broadcast

                # Both succeeded - add to table
                self.__add_stream_to_table(stream)

                self.statusbar.showMessage("Stream created successfully", 2000)

            except Exception as error:
                self.__logger.error(f"Error creating stream: {error}")
                self.statusbar.showMessage("Unexpected error creating stream", 5000)

    def remove_stream(self, id_item: QTableWidgetItem):
        """
        Remove a stream from database and table UI.

        :param id_item: QTableWidgetItem reference from the ID column
        :return: None
        """
        try:
            # Get current row index from the item reference
            row = self.streams_table.row(id_item)
            stream_name = self.streams_table.item(row, 1).text()

            # Ask for confirmation before deleting
            if not self.__confirm_deletion(stream_name, "stream"):
                return

            success, msg = self.__manager.delete_stream(stream_name)

            if not success:
                self.statusbar.showMessage(f"Error: {msg}", 5000)
                return

            # Remove row using current index (works even if previous rows were deleted)
            self.streams_table.removeRow(row)

            self.statusbar.showMessage("Stream deleted successfully", 2000)

        except Exception as error:
            self.__logger.error(f"Error removing stream: {error}")
            self.statusbar.showMessage("Unexpected error deleting stream", 5000)

    # ==================================================================================================================
    # TRANSMISSION
    # ==================================================================================================================


if __name__ == "__main__":
    #  pyside6-uic mainwindow.ui -o mainwindow.py
    app = QApplication(sys.argv)
    apply_stylesheet(app, "light_blue.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
