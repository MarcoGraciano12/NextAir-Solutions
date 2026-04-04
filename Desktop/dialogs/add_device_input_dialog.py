"""
Add Device Input Dialog Module

Author: Marco Graciano
Date: 2025-03-31

Description: Dialog for creating and configuring new audio input devices with validation.
"""

import sounddevice as sd
from PySide6.QtCore import Qt
from logging import Logger, getLogger
from PySide6.QtGui import QIntValidator
from resources.add_device_input import Ui_Dialog
from PySide6.QtWidgets import QDialog, QMessageBox, QStyledItemDelegate


class CenterDelegate(QStyledItemDelegate):
    """
    Delegate to center align combo box items.
    """

    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.displayAlignment = Qt.AlignCenter


class AddDeviceDialog(QDialog):
    """
    Dialog for adding new audio input device configurations.

    Provides form interface to configure device name, audio parameters,
    and GPIO pins. Automatically detects available audio devices using sounddevice.
    """
    def __init__(self, parent=None, logger: Logger = None):
        """
        Dialog for adding a new device input.

        :param parent: Parent widget (MainWindow)
        :param logger: Logger instance
        """
        super().__init__(parent)

        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.__logger = logger or getLogger(self.__class__.__name__)

        # Center align all combo boxes
        for combo in [self.ui.devices_combo, self.ui.sample_rate_combo, self.ui.block_size_combo, self.ui.channels_combo]:
            combo.setItemDelegate(CenterDelegate(combo))
            # Center the displayed text when closed
            combo.setEditable(True)
            combo.lineEdit().setReadOnly(True)
            combo.lineEdit().setAlignment(Qt.AlignCenter)

        # Set validators for numeric inputs (1-100)
        gpi_validator = QIntValidator(1, 100, self)
        gpo_validator = QIntValidator(1, 100, self)

        self.ui.gpi_line.setValidator(gpi_validator)
        self.ui.gpo_line.setValidator(gpo_validator)

        # Add placeholder for sample rate combo
        # self.ui.sample_rate_combo.insertItem(0, "Select sample rate")

        # Device name combo
        self.ui.devices_combo.addItem("Select audio device", None)
        self.ui.devices_combo.setCurrentIndex(0)

        # Samplerate combo
        self.ui.sample_rate_combo.addItem("Select sample rate", None)
        self.ui.sample_rate_combo.addItem("44100", 44100)
        self.ui.sample_rate_combo.addItem("48000", 48000)
        self.ui.sample_rate_combo.setCurrentIndex(0)

        # Blocksize combo
        self.ui.block_size_combo.addItem("Select block size", None)
        self.ui.block_size_combo.addItem("512", 512)
        self.ui.block_size_combo.addItem("1024", 1024)
        self.ui.block_size_combo.addItem("2048", 2048)
        self.ui.block_size_combo.addItem("4096", 4096)
        self.ui.block_size_combo.setCurrentIndex(0)

        # Channels combo
        self.ui.channels_combo.addItem("Select channels", None)
        self.ui.channels_combo.addItem("1", 1)
        self.ui.channels_combo.addItem("2", 2)
        self.ui.channels_combo.setCurrentIndex(0)

        # Connect sample_rate selection to device loading
        # self.ui.devices_combo.activated.connect(self.load_audio_devices)
        self.ui.sample_rate_combo.activated.connect(self.load_audio_devices)
        self.ui.channels_combo.activated.connect(self.load_audio_devices)

        # Connect buttons
        self.ui.create_button.clicked.connect(self.__validate_and_accept)
        self.ui.cancel_button.clicked.connect(self.reject)

    def load_audio_devices(self) -> None:
        """
        Loads audio input devices that support the selected sample rate.

        :return: None
        """
        sample_rate = self.ui.sample_rate_combo.currentData()

        if not sample_rate:
            return

        channels = self.ui.channels_combo.currentData()

        if not channels:
            return

        try:
            devices = sd.query_devices()

            self.ui.devices_combo.clear()

            # Add placeholder as first item
            self.ui.devices_combo.addItem("Select audio device", None)

            for idx, device in enumerate(devices):
                if device['default_samplerate'] == sample_rate and device['max_input_channels'] >= channels:
                    self.ui.devices_combo.addItem(device['name'], idx)

        except Exception as error:
            self.__logger.error(f"Failed to load audio devices: {error}")
            QMessageBox.critical(self, "Device Error", f"Failed to detect audio devices:\n{error}")

    def __validate_and_accept(self) -> None:
        """
        Validates form fields before accepting dialog.

        :return: None
        """
        name = self.ui.name_line.text().strip()

        if not name:
            QMessageBox.warning(self, "Missing Information", "Please enter a name for the device")
            return

        if self.ui.devices_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information", "Please select an audio device from the list")
            return

        if self.ui.sample_rate_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information", "Please select a sample rate")
            return

        if self.ui.block_size_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information", "Please select a block size")
            return

        if self.ui.channels_combo.currentData() is None:
            QMessageBox.warning(self, "Missing Information", "Please select the number of channels")
            return

        self.accept()

    def get_device_data(self) -> dict:
        """
        Retrieves device input data from form fields.

        :return: Dictionary with device configuration
        """
        return {
            'name': self.ui.name_line.text().strip(),
            'device_name': self.ui.devices_combo.currentText(),
            'sample_rate': int(self.ui.sample_rate_combo.currentText()),
            'block_size': int(self.ui.block_size_combo.currentText()),
            'channels': int(self.ui.channels_combo.currentText()),
            'gpi': int(self.ui.gpi_line.text()) if self.ui.gpi_line.text() else None,
            'gpo': int(self.ui.gpo_line.text()) if self.ui.gpo_line.text() else None
        }
