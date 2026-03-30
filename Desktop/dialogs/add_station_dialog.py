
from logging import Logger, getLogger
from resources.add_station import Ui_Dialog
from PySide6.QtWidgets import QDialog, QFileDialog, QMessageBox


class AddStationDialog(QDialog):
    def __init__(self, parent=None, logger: Logger = None):
        """
        Dialog for adding a new station.

        :param parent: Parent widget (MainWindow)
        :param logger: Logger instance
        """
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.__logger = logger or getLogger(self.__class__.__name__)

        # Connect buttons
        self.ui.create_button.clicked.connect(self.__validate_and_accept)  # OK equivalent
        self.ui.cancel_button.clicked.connect(self.reject)  # Cancel equivalent
        self.ui.search_button.clicked.connect(self.__browse_folder)

    def __browse_folder(self):
        """
        Open file explorer to select a folder path.

        Updates the path input field with selected directory.

        :return: None
        """
        path = QFileDialog.getExistingDirectory(
            self,
            "Select Files Directory",
            "",
            QFileDialog.ShowDirsOnly
        )

        if path:
            self.ui.path_line.setText(path)

    def get_station_data(self) -> dict:
        """
        Get station data from dialog inputs.

        :return: Dictionary with 'name' and 'path' keys
        """
        return {
            'name': self.ui.name_line.text(),
            'path': self.ui.path_line.text()
        }

    def __validate_and_accept(self):
        """
        Validate input fields before accepting dialog.

        Shows error message if required fields are empty.

        :return: None
        """
        name = self.ui.name_line.text().strip()
        path = self.ui.path_line.text().strip()

        # Check for empty fields
        if not name or not path:
            QMessageBox.warning(
                self,
                "Missing Information",
                "Please fill in both station name and files path.",
                QMessageBox.Ok
            )
            return

        # Validation passed - close dialog with Accepted
        self.accept()
