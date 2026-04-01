from PySide6.QtCore import Qt
from logging import Logger, getLogger
from PySide6.QtGui import QIntValidator
from resources.add_stream import Ui_Dialog
from PySide6.QtWidgets import QDialog, QMessageBox, QStyledItemDelegate


class CenterDelegate(QStyledItemDelegate):
    """
    Delegate to center align combo box items.
    """

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class AddStreamDialog(QDialog):

    def __init__(self, stations_data: list = None, parent=None, logger: Logger = None):
        """
        Dialog for adding a new stream.

        :param parent: Parent widget (MainWindow)
        :param logger: Logger instance
        """
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.__logger = logger or getLogger(self.__class__.__name__)

        # Center align all combo boxes
        for combo in [self.ui.stations_combo, self.ui.channels_combo, self.ui.sample_rate_combo, self.ui.block_size_combo, self.ui.bit_rate_combo]:
            combo.setItemDelegate(CenterDelegate(combo))
            # Center the displayed text when closed
            combo.setEditable(True)
            combo.lineEdit().setReadOnly(True)
            combo.lineEdit().setAlignment(Qt.AlignCenter)

        # Populate stations combo with provided data
        self.ui.stations_combo.addItem("SELECT STATION", None)
        if stations_data:
            for station_id, station_name in stations_data:
                self.ui.stations_combo.addItem(station_name, station_id)

        # Set validators for numeric inputs (1-100)
        external_id_validator = QIntValidator(1, 100, self)
        self.ui.external_id_line.setValidator(external_id_validator)

        # Set placeholder as selected by default
        self.ui.stations_combo.setCurrentIndex(0)

        # Channels combo
        self.ui.channels_combo.addItem("Select channels...", None)
        self.ui.channels_combo.addItem("1", 1)
        self.ui.channels_combo.addItem("2", 2)
        self.ui.channels_combo.setCurrentIndex(0)

        # Sample rate combo
        self.ui.sample_rate_combo.addItem("Select sample rate...", None)
        self.ui.sample_rate_combo.addItem("44100", 44100)
        self.ui.sample_rate_combo.addItem("48000", 48000)
        self.ui.sample_rate_combo.setCurrentIndex(0)

        # Block size combo
        self.ui.block_size_combo.addItem("Select block size...", None)
        self.ui.block_size_combo.addItem("512", 512)
        self.ui.block_size_combo.addItem("1024", 1024)
        self.ui.block_size_combo.addItem("2048", 2048)
        self.ui.block_size_combo.addItem("4096", 4096)
        self.ui.block_size_combo.setCurrentIndex(0)

        # Bit rate combo (store as string with 'k')
        self.ui.bit_rate_combo.addItem("Select bit rate...", None)
        self.ui.bit_rate_combo.addItem("128k", "128k")
        self.ui.bit_rate_combo.addItem("192k", "192k")
        self.ui.bit_rate_combo.addItem("256k", "256k")
        self.ui.bit_rate_combo.addItem("320k", "320k")
        self.ui.bit_rate_combo.setCurrentIndex(0)

        # Center align text in input fields
        for line_edit in [self.ui.name_line, self.ui.external_id_line, self.ui.url_line, self.ui.user_line, self.ui.password_line]:
            line_edit.setAlignment(Qt.AlignCenter)

        # Connect buttons
        self.ui.create_button.clicked.connect(self.__validate_and_accept)
        self.ui.cancel_button.clicked.connect(self.reject)

    def __validate_and_accept(self):
        """
        Validate input fields before accepting dialog.

        Checks that all required fields are filled and combo boxes have
        valid selections (not placeholders).

        :return: None
        """
        # Validate combo boxes (check for None = placeholder selected)
        if self.ui.stations_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information","Please select a station.", QMessageBox.Ok)
            return

        if self.ui.channels_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information","Please select channels.", QMessageBox.Ok)
            return

        if self.ui.sample_rate_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information","Please select sample rate.", QMessageBox.Ok)
            return

        if self.ui.block_size_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information","Please select block size.", QMessageBox.Ok)
            return

        if self.ui.bit_rate_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information","Please select bit rate.", QMessageBox.Ok)
            return

        # Validate text fields (strip whitespace and check if empty)
        name = self.ui.name_line.text().strip()
        external_id = self.ui.external_id_line.text().strip()
        url = self.ui.url_line.text().strip()
        user = self.ui.user_line.text().strip()
        password = self.ui.password_line.text().strip()

        if not name or not external_id or not url or not user or not password:
            QMessageBox.warning(self, "Missing Information","Please fill in all required fields.", QMessageBox.Ok)
            return

        # All validations passed
        self.accept()

    def get_stream_data(self) -> dict:
        """
        Get stream data from dialog inputs.

        :return: Dictionary with all stream configuration data
        """
        return {
            'station_id': self.ui.stations_combo.currentData(),
            'name': self.ui.name_line.text().strip(),
            'external_id': self.ui.external_id_line.text().strip(),
            'url': self.ui.url_line.text().strip(),
            'user': self.ui.user_line.text().strip(),
            'password': self.ui.password_line.text().strip(),
            'channels': self.ui.channels_combo.currentData(),
            'sample_rate': self.ui.sample_rate_combo.currentData(),
            'block_size': self.ui.block_size_combo.currentData(),
            'bit_rate': self.ui.bit_rate_combo.currentData()
        }
