# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_device_input.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFormLayout,
    QFrame, QGridLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(379, 409)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.formLayout = QFormLayout(self.widget)
        self.formLayout.setObjectName(u"formLayout")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_2)

        self.name_line = QLineEdit(self.widget)
        self.name_line.setObjectName(u"name_line")
        self.name_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.name_line)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.devices_combo = QComboBox(self.widget)
        self.devices_combo.setObjectName(u"devices_combo")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.devices_combo)

        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.sample_rate_combo = QComboBox(self.widget)
        self.sample_rate_combo.setObjectName(u"sample_rate_combo")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.sample_rate_combo)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.gpi_line = QLineEdit(self.widget)
        self.gpi_line.setObjectName(u"gpi_line")
        self.gpi_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.gpi_line)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.gpo_line = QLineEdit(self.widget)
        self.gpo_line.setObjectName(u"gpo_line")
        self.gpo_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.gpo_line)


        self.verticalLayout.addWidget(self.widget)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.widget_2 = QWidget(self.frame)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.create_button = QPushButton(self.widget_2)
        self.create_button.setObjectName(u"create_button")

        self.horizontalLayout.addWidget(self.create_button)

        self.line_3 = QFrame(self.widget_2)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.cancel_button = QPushButton(self.widget_2)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontalLayout.addWidget(self.cancel_button)


        self.verticalLayout.addWidget(self.widget_2)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt; font-weight:700;\">CREATE DEVICE INPUT</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">NAME:</span></p></body></html>", None))
        self.name_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"Type device name", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">DEVICE NAME:</span></p></body></html>", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">SAMPLERATE:</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">GPI:</span></p></body></html>", None))
        self.gpi_line.setInputMask("")
        self.gpi_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"Type gpi number", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:10pt; font-weight:700;\">GPO:</span></p></body></html>", None))
        self.gpo_line.setInputMask("")
        self.gpo_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"Type gpo number", None))
        self.create_button.setText(QCoreApplication.translate("Dialog", u"CREATE", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"CANCEL", None))
    # retranslateUi

