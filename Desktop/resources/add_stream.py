# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_stream.ui'
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
        Dialog.resize(525, 673)
        self.gridLayout = QGridLayout(Dialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget = QWidget(self.frame)
        self.widget.setObjectName(u"widget")
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)


        self.verticalLayout.addWidget(self.widget)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.widget_2 = QWidget(self.frame)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.widget_5 = QWidget(self.widget_2)
        self.widget_5.setObjectName(u"widget_5")
        self.formLayout = QFormLayout(self.widget_5)
        self.formLayout.setObjectName(u"formLayout")
        self.label_3 = QLabel(self.widget_5)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label_3)

        self.name_line = QLineEdit(self.widget_5)
        self.name_line.setObjectName(u"name_line")
        self.name_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(1, QFormLayout.ItemRole.FieldRole, self.name_line)

        self.label_4 = QLabel(self.widget_5)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.ItemRole.LabelRole, self.label_4)

        self.external_id_line = QLineEdit(self.widget_5)
        self.external_id_line.setObjectName(u"external_id_line")
        self.external_id_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(2, QFormLayout.ItemRole.FieldRole, self.external_id_line)

        self.label_5 = QLabel(self.widget_5)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(3, QFormLayout.ItemRole.LabelRole, self.label_5)

        self.url_line = QLineEdit(self.widget_5)
        self.url_line.setObjectName(u"url_line")
        self.url_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(3, QFormLayout.ItemRole.FieldRole, self.url_line)

        self.label_6 = QLabel(self.widget_5)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(4, QFormLayout.ItemRole.LabelRole, self.label_6)

        self.user_line = QLineEdit(self.widget_5)
        self.user_line.setObjectName(u"user_line")
        self.user_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(4, QFormLayout.ItemRole.FieldRole, self.user_line)

        self.label_7 = QLabel(self.widget_5)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(5, QFormLayout.ItemRole.LabelRole, self.label_7)

        self.password_line = QLineEdit(self.widget_5)
        self.password_line.setObjectName(u"password_line")
        self.password_line.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)
        self.password_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.formLayout.setWidget(5, QFormLayout.ItemRole.FieldRole, self.password_line)

        self.label_8 = QLabel(self.widget_5)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(6, QFormLayout.ItemRole.LabelRole, self.label_8)

        self.label_9 = QLabel(self.widget_5)
        self.label_9.setObjectName(u"label_9")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.LabelRole, self.label_9)

        self.sample_rate_combo = QComboBox(self.widget_5)
        self.sample_rate_combo.setObjectName(u"sample_rate_combo")

        self.formLayout.setWidget(7, QFormLayout.ItemRole.FieldRole, self.sample_rate_combo)

        self.label_10 = QLabel(self.widget_5)
        self.label_10.setObjectName(u"label_10")

        self.formLayout.setWidget(8, QFormLayout.ItemRole.LabelRole, self.label_10)

        self.block_size_combo = QComboBox(self.widget_5)
        self.block_size_combo.setObjectName(u"block_size_combo")
        self.block_size_combo.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.block_size_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContentsOnFirstShow)

        self.formLayout.setWidget(8, QFormLayout.ItemRole.FieldRole, self.block_size_combo)

        self.label_11 = QLabel(self.widget_5)
        self.label_11.setObjectName(u"label_11")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.LabelRole, self.label_11)

        self.bit_rate_combo = QComboBox(self.widget_5)
        self.bit_rate_combo.setObjectName(u"bit_rate_combo")

        self.formLayout.setWidget(9, QFormLayout.ItemRole.FieldRole, self.bit_rate_combo)

        self.channels_combo = QComboBox(self.widget_5)
        self.channels_combo.setObjectName(u"channels_combo")
        self.channels_combo.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.channels_combo.setFrame(True)

        self.formLayout.setWidget(6, QFormLayout.ItemRole.FieldRole, self.channels_combo)

        self.label_12 = QLabel(self.widget_5)
        self.label_12.setObjectName(u"label_12")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.label_12)

        self.stations_combo = QComboBox(self.widget_5)
        self.stations_combo.setObjectName(u"stations_combo")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.stations_combo)


        self.verticalLayout_3.addWidget(self.widget_5)


        self.verticalLayout.addWidget(self.widget_2)

        self.line = QFrame(self.frame)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.widget_3 = QWidget(self.frame)
        self.widget_3.setObjectName(u"widget_3")
        self.horizontalLayout = QHBoxLayout(self.widget_3)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.create_button = QPushButton(self.widget_3)
        self.create_button.setObjectName(u"create_button")

        self.horizontalLayout.addWidget(self.create_button)

        self.line_3 = QFrame(self.widget_3)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_3)

        self.cancel_button = QPushButton(self.widget_3)
        self.cancel_button.setObjectName(u"cancel_button")

        self.horizontalLayout.addWidget(self.cancel_button)


        self.verticalLayout.addWidget(self.widget_3)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_4)


        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:700;\">CREATE STREAM</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">STREAM NAME:</span></p></body></html>", None))
        self.name_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"STREAM NAME", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">EXTERNAL ID:</span></p></body></html>", None))
        self.external_id_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"EXTERNAL DATABASE ID", None))
        self.label_5.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">URL:</span></p></body></html>", None))
        self.url_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"STREAM URL", None))
        self.label_6.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">USER:</span></p></body></html>", None))
        self.user_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"BROADCAST USER", None))
        self.label_7.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">PASSWORD:</span></p></body></html>", None))
        self.password_line.setPlaceholderText(QCoreApplication.translate("Dialog", u"BROADCAST PASSWORD", None))
        self.label_8.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">CHANNELS:</span></p></body></html>", None))
        self.label_9.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">SAMPLERATE</span></p></body></html>", None))
        self.sample_rate_combo.setCurrentText("")
        self.sample_rate_combo.setPlaceholderText(QCoreApplication.translate("Dialog", u"SELECT  SAMPLERATE", None))
        self.label_10.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">BLOCKSIZE:</span></p></body></html>", None))
        self.block_size_combo.setPlaceholderText(QCoreApplication.translate("Dialog", u"SELECT  BLOCKSIZE", None))
        self.label_11.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">BITRATE</span></p></body></html>", None))
        self.bit_rate_combo.setPlaceholderText(QCoreApplication.translate("Dialog", u"SELECT  BITRATE", None))
        self.channels_combo.setPlaceholderText(QCoreApplication.translate("Dialog", u"SELECT CHANNELS", None))
        self.label_12.setText(QCoreApplication.translate("Dialog", u"<html><head/><body><p><span style=\" font-size:12pt; font-weight:700;\">STATION:</span></p></body></html>", None))
        self.stations_combo.setPlaceholderText(QCoreApplication.translate("Dialog", u"SELECT STATION", None))
        self.create_button.setText(QCoreApplication.translate("Dialog", u"CREATE", None))
        self.cancel_button.setText(QCoreApplication.translate("Dialog", u"CANCEL", None))
    # retranslateUi

