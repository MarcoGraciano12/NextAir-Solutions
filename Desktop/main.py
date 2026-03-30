"""
Main application entry point.

Author: Marco
Date: 2025-03-25
"""

import sys
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
from dialogs import AddStationDialog


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
        self.__setup_streams_table()
        self.__setup_stations_table()

        self.__load_stations_table()

        self.login_button.pressed.connect(self.login)
        self.logout_button.pressed.connect(self.logout)

        self.theme_combo.currentIndexChanged.connect(self.change_theme)

        # TabWidget Main Menu
        self.__initialized_tabs = set()  # Track initialized tabs
        self.menu_tab.currentChanged.connect(self.__on_menu_tab_changed)

        # STATION ACTIONS
        self.add_station_button.pressed.connect(self.add_station)



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

    def __on_menu_tab_changed(self, index: int):
        """
        Handle tab change.

        :param index: Tab index (passed automatically by signal)
        """
        if index in self.__initialized_tabs:
            return  # Already initialized

        if index == 3:
            self.load_streams()

        self.__initialized_tabs.add(index)  # Mark as initialized

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

    # ==================================================================================================================
    # USERS
    # ==================================================================================================================
    def add_stream(self):
        pass

    def delete_stream(self):
        pass

    def edit_stream(self):
        pass

    def find_stream(self):
        pass

    def __setup_streams_table(self):
        """
        Setup streams table structure and properties.

        :return: None
        """
        columns = ["stream_id", "station_id", "external_id", "stream_name", "Actions"]

        self.streams_table.setColumnCount(len(columns))
        self.streams_table.setHorizontalHeaderLabels(columns)
        self.streams_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.streams_table.setSelectionBehavior(QTableWidget.SelectRows)

        # All columns stretch proportionally
        self.streams_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.streams_table.verticalHeader().setDefaultSectionSize(40)

    def load_streams(self):
        """
        Load all streams from database into table.

        :return: None
        """
        try:
            # Fetch streams from database
            streams = self.__manager.get_all_streams()

            # Check if streams exist
            if not streams:
                self.__logger.warning("No streams found in database")
                self.statusbar.showMessage("No streams available", 3000)
                return

            # Clear table and set row count
            self.streams_table.setRowCount(0)
            self.streams_table.setRowCount(len(streams))

            # Populate table rows
            for i, stream in enumerate(streams):
                # Set stream data columns
                self.streams_table.setItem(i, 0, QTableWidgetItem(str(stream.stream_id)))
                self.streams_table.setItem(i, 1, QTableWidgetItem(str(stream.station_id)))
                self.streams_table.setItem(i, 2, QTableWidgetItem(str(stream.external_id)))
                self.streams_table.setItem(i, 3, QTableWidgetItem(str(stream.stream_name)))

                # Create action buttons
                edit_btn = QPushButton("Edit")
                delete_btn = QPushButton("Delete")

                # Connect button signals
                # edit_btn.clicked.connect(lambda checked, row=i: self.__edit_stream(row))
                # delete_btn.clicked.connect(lambda checked, row=i: self.__delete_stream(row))

                # Create container widget for buttons
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.addWidget(edit_btn)
                actions_layout.addWidget(delete_btn)
                actions_layout.setContentsMargins(0, 0, 0, 0)

                # Add buttons to Actions column
                self.streams_table.setCellWidget(i, 4, actions_widget)

            self.__logger.info(f"Loaded {len(streams)} streams successfully")
            self.statusbar.showMessage(f"Loaded {len(streams)} streams", 3000)

        except Exception as error:
            self.__logger.error(f"Failed to load streams: {str(error)}")
            self.statusbar.showMessage("Error loading streams", 3000)


        # # Login Page
        # self.stackedWidget.setCurrentIndex(0)
        #
        # # Themes
        # self.__setup_theme_actions()
        #
        # self.menubar.setVisible(False)
        #
        # self.sing_in_pushButton.clicked.connect(self.__login)
        # self.password_lineEdit.returnPressed.connect(self.__login)
        #
        # self.logout_button.clicked.connect(self.__logout)
        #
        # # USERS
        # self.users_create_button.clicked.connect(self.create_user)
        # self.manage_users.triggered.connect(self.show_users_page)
        # self.users_return_button.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        # self.__setup_users_table()

    # ==================================================================================================================
    # STATIONS
    # ==================================================================================================================
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

        # Create action buttons for the new row
        edit_btn = QPushButton("Edit")
        delete_btn = QPushButton("Delete")

        # Connect delete button with item reference
        delete_btn.clicked.connect(lambda checked, item=id_item: self.remove_station(item))

        # Create widget container for buttons
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.setContentsMargins(0, 0, 0, 0)

        self.stations_table.setCellWidget(row, 3, actions_widget)

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

            # Clear existing rows to avoid duplicates
            self.stations_table.setRowCount(0)
            self.stations_table.setRowCount(len(stations))

            for i, station in enumerate(stations):
                # Create centered items for all columns
                id_item = QTableWidgetItem(str(station.station_id))
                id_item.setTextAlignment(Qt.AlignCenter)

                name_item = QTableWidgetItem(str(station.station_name))
                name_item.setTextAlignment(Qt.AlignCenter)

                path_item = QTableWidgetItem(str(station.files_path))
                path_item.setTextAlignment(Qt.AlignCenter)

                self.stations_table.setItem(i, 0, id_item)
                self.stations_table.setItem(i, 1, name_item)
                self.stations_table.setItem(i, 2, path_item)

                # Create action buttons for each station row
                edit_btn = QPushButton("Edit")
                delete_btn = QPushButton("Delete")

                # Connect button signals
                delete_btn.clicked.connect(lambda checked, item=id_item: self.remove_station(item))

                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.addWidget(edit_btn)
                actions_layout.addWidget(delete_btn)
                actions_layout.setContentsMargins(0, 0, 0, 0)

                self.stations_table.setCellWidget(i, 3, actions_widget)

            self.__logger.info(f"Loaded {len(stations)} stations into table")
            self.statusbar.showMessage(f"{len(stations)} stations loaded successfully", 2000)

        except Exception as error:
            self.__logger.error(f"Failed to load stations table: {error}")
            self.statusbar.showMessage("Error loading stations. Check logs for details.", 5000)

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

            self.statusbar.showMessage("Station deleted successfully", 2000)

        except Exception as error:
            self.__logger.error(f"Error removing station: {error}")
            self.statusbar.showMessage("Unexpected error deleting station", 5000)

    def edit_station(self):
        pass

    def find_station(self):
        pass


    # ==================================================================================================================
    # STREAMS
    # ==================================================================================================================

    # ==================================================================================================================
    # TRANSMISSION
    # ==================================================================================================================
    #
    # @staticmethod
    # def change_theme(theme_name: str) -> None:
    #     """
    #     Apply new stylesheet theme to application.
    #
    #     :param theme_name: Theme file name (e.g., "light_blue.xml")
    #     :return: None
    #     """
    #     app = QApplication.instance()
    #     apply_stylesheet(app, theme=theme_name)
    #
    # def __setup_theme_actions(self):
    #     self.dark_amber.triggered.connect(lambda: self.change_theme("dark_amber.xml"))
    #     self.dark_blue.triggered.connect(lambda: self.change_theme("dark_blue.xml"))
    #     self.dark_cyan.triggered.connect(lambda: self.change_theme("dark_cyan.xml"))
    #     self.dark_green.triggered.connect(lambda: self.change_theme("dark_lightgreen.xml"))
    #     self.dark_pink.triggered.connect(lambda: self.change_theme("dark_pink.xml"))
    #     self.dark_purple.triggered.connect(lambda: self.change_theme("dark_purple.xml"))
    #     self.dark_red.triggered.connect(lambda: self.change_theme("dark_red.xml"))
    #     self.dark_teal.triggered.connect(lambda: self.change_theme("dark_teal.xml"))
    #     self.dark_yellow.triggered.connect(lambda: self.change_theme("dark_yellow.xml"))
    #
    #     self.light_amber.triggered.connect(lambda: self.change_theme("light_amber.xml"))
    #     self.light_blue.triggered.connect(lambda: self.change_theme("light_blue.xml"))
    #     self.light_cyan.triggered.connect(lambda: self.change_theme("light_cyan.xml"))
    #     self.light_cyan_500.triggered.connect(lambda: self.change_theme("light_cyan_500.xml"))
    #     self.light_green.triggered.connect(lambda: self.change_theme("light_lightgreen.xml"))
    #     self.light_pink.triggered.connect(lambda: self.change_theme("light_pink.xml"))
    #     self.light_purple.triggered.connect(lambda: self.change_theme("light_purple.xml"))
    #     self.light_red.triggered.connect(lambda: self.change_theme("light_red.xml"))
    #     self.light_teal.triggered.connect(lambda: self.change_theme("light_teal.xml"))
    #     self.light_yellow.triggered.connect(lambda: self.change_theme("light_yellow.xml"))
    #
    # def __setup_users_table(self) -> None:
    #     """
    #     Configure users table columns and properties.
    #
    #     :return: None
    #     """
    #     columns = ["ID", "Username", "Name", "Last Name", "Role", "Actions"]
    #     self.users_table.setColumnCount(len(columns))
    #     self.users_table.setHorizontalHeaderLabels(columns)
    #     self.users_table.setEditTriggers(QTableWidget.NoEditTriggers)
    #     self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
    #
    #     # Adjust column widths
    #     self.users_table.horizontalHeader().setStretchLastSection(True)
    #     self.users_table.setColumnWidth(0, 50)  # ID
    #     self.users_table.setColumnWidth(1, 120)  # Username
    #     self.users_table.setColumnWidth(2, 150)  # Name
    #     self.users_table.setColumnWidth(3, 150)  # Last Name
    #     self.users_table.setColumnWidth(4, 100)  # Role
    #
    # def __login(self):
    #     """
    #     Authenticate user credentials and handle login process.
    #
    #     :return: None
    #     """
    #     username = self.username_lineEdit.text().strip()
    #     password = self.password_lineEdit.text().strip()
    #
    #     if not username or not password:
    #         self.__logger.warning("Empty credentials provided")
    #         self.statusBar().showMessage("Please enter username and password", 3000)
    #         return
    #
    #     session = setup.db_manager.get_session()
    #     user = User.find_by_username(session, username)
    #
    #     if user and pbkdf2_sha256.verify(password, user.password):
    #         self.__logger.info(f"User authenticated: {username}")
    #         self.statusBar().showMessage(f"Welcome {user.name} {user.last_name}!", 5000)
    #         self.menubar.setVisible(True)
    #         self.stackedWidget.setCurrentIndex(1)
    #     else:
    #         self.__logger.warning(f"Invalid credentials for: {username}")
    #         self.statusBar().showMessage("Invalid username or password", 3000)
    #
    #     session.close()
    #
    # def __logout(self):
    #     """
    #     Clear login fields and return to login screen.
    #
    #     :return: None
    #     """
    #     self.username_lineEdit.clear()
    #     self.password_lineEdit.clear()
    #     self.statusBar().clearMessage()
    #     self.menubar.setVisible(False)
    #     self.stackedWidget.setCurrentIndex(0)
    #     self.__logger.info("User logged out")
    #
    # # ==================================================================================================================
    # # USERS
    # # ==================================================================================================================
    # def load_users(self) -> None:
    #     """
    #     Load users from database and populate table.
    #
    #     :return: None
    #     """
    #     self.users_table.setRowCount(0)
    #
    #     try:
    #         session = setup.db_manager.get_session()
    #         users = User.get_all(session)
    #
    #         for i, user in enumerate(users):
    #             self.users_table.insertRow(i)
    #             self.users_table.setItem(i, 0, QTableWidgetItem(str(user.id)))
    #             self.users_table.setItem(i, 1, QTableWidgetItem(user.username))
    #             self.users_table.setItem(i, 2, QTableWidgetItem(user.name))
    #             self.users_table.setItem(i, 3, QTableWidgetItem(user.last_name))
    #             self.users_table.setItem(i, 4, QTableWidgetItem(user.role))
    #
    #             # Actions buttons
    #             edit_btn = QPushButton("Edit")
    #             delete_btn = QPushButton("Delete")
    #
    #             # Connect with user ID and row index
    #             edit_btn.clicked.connect(lambda checked, row=i, uid=user.id: self.edit_user(uid, row))
    #             delete_btn.clicked.connect(lambda checked, row=i, uid=user.id: self.delete_user(uid, row))
    #
    #             # Container widget for buttons
    #             actions_widget = QWidget()
    #             actions_layout = QHBoxLayout(actions_widget)
    #             actions_layout.addWidget(edit_btn)
    #             actions_layout.addWidget(delete_btn)
    #             actions_layout.setContentsMargins(0, 0, 0, 0)
    #
    #             self.users_table.setCellWidget(i, 5, actions_widget)
    #
    #     except Exception as e:
    #         self.__logger.error(f"Error loading users: {e}")
    #         self.statusBar().showMessage(f"Error loading users: {e}", 5000)
    #
    # def show_users_page(self) -> None:
    #     """
    #     Load users and switch to users management page.
    #
    #     :return: None
    #     """
    #     self.load_users()
    #     self.stackedWidget.setCurrentIndex(2)
    #
    # def delete_user(self, user_id: int, row: int) -> None:
    #     """
    #     Delete user from database after confirmation.
    #
    #     :param user_id: ID of user to delete
    #     :param row: Row index in table
    #     :return: None
    #     """
    #     reply = QMessageBox.question(
    #         self,
    #         "Confirm Delete",
    #         "Are you sure you want to delete this user?",
    #         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    #     )
    #
    #     if reply == QMessageBox.StandardButton.Yes:
    #         try:
    #             session = setup.db_manager.get_session()
    #             user = User.find_by_id(session, user_id)
    #
    #             if user and user.delete_from_db(session):
    #                 self.users_table.removeRow(row)
    #                 self.__logger.info(f"User {user_id} deleted")
    #                 self.statusBar().showMessage(f"User {user_id} deleted", 5000)
    #             else:
    #                 self.__logger.error(f"Failed to delete user {user_id}")
    #                 self.statusBar().showMessage(f"Failed to delete user {user_id}", 5000)
    #
    #         except Exception as e:
    #             self.__logger.error(f"Error deleting user: {e}")
    #             self.statusBar().showMessage(f"Error deleting user: {e}", 5000)
    #
    # def edit_user(self, user_id: int, row: int) -> None:
    #     """
    #     Open dialog to edit user information.
    #
    #     :param user_id: ID of user to edit
    #     :param row: Row index in table
    #     :return: None
    #     """
    #
    #     try:
    #         session = setup.db_manager.get_session()
    #         user = User.find_by_id(session, user_id)
    #
    #         if not user:
    #             self.__logger.error(f"User {user_id} not found")
    #             self.statusBar().showMessage(f"User {user_id} not found", 5000)
    #             return
    #
    #         # Create dialog
    #         dialog = QDialog(self)
    #         dialog.setWindowTitle("Edit User")
    #         layout = QFormLayout(dialog)
    #
    #         # Input fields
    #         username_input = QLineEdit(user.username)
    #         name_input = QLineEdit(user.name)
    #         lastname_input = QLineEdit(user.last_name)
    #         role_combo = QComboBox()
    #         role_combo.addItems(["admin", "user"])
    #         role_combo.setCurrentText(user.role)
    #         password_input = QLineEdit()
    #         password_input.setPlaceholderText("Leave empty to keep current")
    #         password_input.setEchoMode(QLineEdit.EchoMode.Password)
    #
    #         layout.addRow("Username:", username_input)
    #         layout.addRow("Name:", name_input)
    #         layout.addRow("Last Name:", lastname_input)
    #         layout.addRow("Role:", role_combo)
    #         layout.addRow("Password:", password_input)
    #
    #         # Buttons
    #         buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    #         buttons.accepted.connect(
    #             lambda: self.__handle_user_edit(dialog, session, user, username_input, name_input, lastname_input,
    #                                             role_combo, password_input, row))
    #         buttons.rejected.connect(dialog.reject)
    #
    #         layout.addRow(buttons)
    #         dialog.exec()
    #
    #     except Exception as e:
    #         self.__logger.error(f"Error opening edit dialog: {e}")
    #         self.statusBar().showMessage(f"Error opening edit dialog: {e}", 5000)
    #
    # @staticmethod
    # def __save_user_edit(dialog, user, username_input, name_input, lastname_input, role_combo, password_input):
    #     """
    #     Validate and update user data.
    #
    #     :param dialog: Dialog instance
    #     :param user: User instance to update
    #     :param username_input: Username input field
    #     :param name_input: Name input field
    #     :param lastname_input: Last name input field
    #     :param role_combo: Role combobox
    #     :param password_input: Password input field
    #     :return: Updated user if valid, None otherwise
    #     """
    #     new_username = username_input.text().strip()
    #
    #     # Validate username uniqueness (if changed)
    #     if new_username != user.username:
    #         session = setup.db_manager.get_session()
    #         existing = User.find_by_username(session, new_username)
    #
    #         if existing:
    #             QMessageBox.warning(dialog, "Error", "Username already exists")
    #             return None
    #
    #     # Update user data
    #     user.username = new_username
    #     user.name = name_input.text().strip()
    #     user.last_name = lastname_input.text().strip()
    #     user.role = role_combo.currentText()
    #
    #     # Update password only if provided
    #     new_password = password_input.text().strip()
    #     if new_password:
    #         user.password = pbkdf2_sha256.hash(new_password)
    #
    #     return user
    #
    # def __handle_user_edit(self, dialog, session, user, username_input, name_input, lastname_input, role_combo,
    #                        password_input, row) -> None:
    #     """
    #     Handle user edit save.
    #     """
    #     updated_user = self.__save_user_edit(dialog, user, username_input, name_input, lastname_input, role_combo,
    #                                          password_input)
    #
    #     if updated_user and updated_user.save_to_db(session):
    #         # Update table
    #         self.users_table.setItem(row, 1, QTableWidgetItem(updated_user.username))
    #         self.users_table.setItem(row, 2, QTableWidgetItem(updated_user.name))
    #         self.users_table.setItem(row, 3, QTableWidgetItem(updated_user.last_name))
    #         self.users_table.setItem(row, 4, QTableWidgetItem(updated_user.role))
    #
    #         dialog.accept()
    #         self.__logger.info(f"User {updated_user.id} updated")
    #     elif updated_user:
    #         QMessageBox.warning(dialog, "Error", "Failed to save user")
    #
    # def create_user(self) -> None:
    #     """
    #     Open dialog to create new user.
    #
    #     :return: None
    #     """
    #     # Create dialog
    #     dialog = QDialog(self)
    #     dialog.setWindowTitle("Create User")
    #     layout = QFormLayout(dialog)
    #
    #     # Input fields
    #     username_input = QLineEdit()
    #     name_input = QLineEdit()
    #     lastname_input = QLineEdit()
    #     role_combo = QComboBox()
    #     role_combo.addItems(["admin", "user"])
    #     password_input = QLineEdit()
    #     password_input.setEchoMode(QLineEdit.EchoMode.Password)
    #
    #     layout.addRow("Username:", username_input)
    #     layout.addRow("Name:", name_input)
    #     layout.addRow("Last Name:", lastname_input)
    #     layout.addRow("Role:", role_combo)
    #     layout.addRow("Password:", password_input)
    #
    #     # Buttons
    #     buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
    #     buttons.accepted.connect(
    #         lambda: self.__save_new_user(dialog, username_input, name_input, lastname_input, role_combo,
    #                                      password_input))
    #     buttons.rejected.connect(dialog.reject)
    #
    #     layout.addRow(buttons)
    #     dialog.exec()
    #
    # def __save_new_user(self, dialog, username_input, name_input, lastname_input, role_combo, password_input) -> None:
    #     """
    #     Save new user after validation.
    #
    #     :param dialog: Dialog instance to close
    #     :param username_input: Username input field
    #     :param name_input: Name input field
    #     :param lastname_input: Last name input field
    #     :param role_combo: Role combobox
    #     :param password_input: Password input field
    #     :return: None
    #     """
    #     username = username_input.text().strip()
    #     name = name_input.text().strip()
    #     lastname = lastname_input.text().strip()
    #     password = password_input.text().strip()
    #
    #     # Validate required fields
    #     if not all([username, name, lastname, password]):
    #         QMessageBox.warning(dialog, "Error", "All fields are required")
    #         return
    #
    #     # Validate username uniqueness
    #     session = setup.db_manager.get_session()
    #     if User.find_by_username(session, username):
    #         QMessageBox.warning(dialog, "Error", "Username already exists")
    #         return
    #
    #     # Create user
    #     new_user = User(
    #         username=username,
    #         name=name,
    #         last_name=lastname,
    #         role=role_combo.currentText(),
    #         password=pbkdf2_sha256.hash(password)
    #     )
    #
    #     if new_user.save_to_db(session):
    #         # Add to table
    #         row = self.users_table.rowCount()
    #         self.users_table.insertRow(row)
    #         self.users_table.setItem(row, 0, QTableWidgetItem(str(new_user.id)))
    #         self.users_table.setItem(row, 1, QTableWidgetItem(new_user.username))
    #         self.users_table.setItem(row, 2, QTableWidgetItem(new_user.name))
    #         self.users_table.setItem(row, 3, QTableWidgetItem(new_user.last_name))
    #         self.users_table.setItem(row, 4, QTableWidgetItem(new_user.role))
    #
    #         # Add action buttons
    #         edit_btn = QPushButton("Edit")
    #         delete_btn = QPushButton("Delete")
    #         edit_btn.clicked.connect(lambda checked, r=row, uid=new_user.id: self.edit_user(uid, r))
    #         delete_btn.clicked.connect(lambda checked, r=row, uid=new_user.id: self.delete_user(uid, r))
    #
    #         actions_widget = QWidget()
    #         actions_layout = QHBoxLayout(actions_widget)
    #         actions_layout.addWidget(edit_btn)
    #         actions_layout.addWidget(delete_btn)
    #         actions_layout.setContentsMargins(0, 0, 0, 0)
    #
    #         self.users_table.setCellWidget(row, 5, actions_widget)
    #
    #         dialog.accept()
    #         self.__logger.info(f"User {new_user.id} created")
    #     else:
    #         QMessageBox.warning(dialog, "Error", "Failed to create user")
    #



if __name__ == "__main__":
    #  pyside6-uic mainwindow.ui -o mainwindow.py
    app = QApplication(sys.argv)
    apply_stylesheet(app, "light_blue.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
