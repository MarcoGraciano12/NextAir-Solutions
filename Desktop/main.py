"""
Main application entry point.

Author: Marco
Date: 2025-03-25
"""

import setup_logs


import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFormLayout, QWidget, QLineEdit, QPushButton, QLabel
)
from resources.mainwindow import Ui_MainWindow
from qt_material import apply_stylesheet
from setup import setup
from models import User
from logging import Logger, getLogger
from passlib.hash import pbkdf2_sha256


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Main window for testing database connection.
    """

    def __init__(self, logger: Logger = None):
        """
        Initialize main window.
        """
        self.__logger = logger or getLogger(self.__class__.__name__)
        super().__init__()
        self.setupUi(self)

        self.menubar.setVisible(False)

        self.sing_in_pushButton.clicked.connect(self.__login)
        self.password_lineEdit.returnPressed.connect(self.__login)

        self.logout_button.clicked.connect(self.__logout)

    def __login(self):
        """
        Authenticate user credentials and handle login process.

        :return: None
        """
        username = self.username_lineEdit.text().strip()
        password = self.password_lineEdit.text().strip()

        if not username or not password:
            self.__logger.warning("Empty credentials provided")
            self.statusBar().showMessage("Please enter username and password", 3000)
            return

        session = setup.db_manager.get_session()
        user = User.find_by_username(session, username)

        if user and pbkdf2_sha256.verify(password, user.password):
            self.__logger.info(f"User authenticated: {username}")
            self.statusBar().showMessage(f"Welcome {user.name} {user.last_name}!", 5000)
            self.menubar.setVisible(True)
            self.stackedWidget.setCurrentIndex(1)
        else:
            self.__logger.warning(f"Invalid credentials for: {username}")
            self.statusBar().showMessage("Invalid username or password", 3000)

        session.close()

    def __logout(self):
        """
        Clear login fields and return to login screen.

        :return: None
        """
        self.username_lineEdit.clear()
        self.password_lineEdit.clear()
        self.statusBar().clearMessage()
        self.menubar.setVisible(False)
        self.stackedWidget.setCurrentIndex(0)
        self.__logger.info("User logged out")

if __name__ == "__main__":
    if not setup.initialize():
        print("Failed to initialize setup")
        sys.exit(1)

    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="light_blue.xml")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())