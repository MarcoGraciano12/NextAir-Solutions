# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QMenuBar, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(974, 739)
        font = QFont()
        font.setFamilies([u"Yu Gothic UI Semibold"])
        font.setPointSize(20)
        font.setBold(True)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_2 = QGridLayout(self.page)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.frame = QFrame(self.page)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_4 = QWidget(self.frame)
        self.widget_4.setObjectName(u"widget_4")
        self.gridLayout_3 = QGridLayout(self.widget_4)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.label_4 = QLabel(self.widget_4)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout_3.addWidget(self.label_4, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 6, 1, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 3, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 3, 2, 1, 1)

        self.widget_3 = QWidget(self.widget_4)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.login_button = QPushButton(self.widget_3)
        self.login_button.setObjectName(u"login_button")

        self.verticalLayout_2.addWidget(self.login_button)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_6)

        self.label = QLabel(self.widget_3)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)


        self.gridLayout_3.addWidget(self.widget_3, 5, 1, 1, 1)

        self.widget_2 = QWidget(self.widget_4)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_3 = QVBoxLayout(self.widget_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.username_line = QLineEdit(self.widget_2)
        self.username_line.setObjectName(u"username_line")

        self.verticalLayout_3.addWidget(self.username_line)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_4)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_3.addWidget(self.label_2)

        self.password_line = QLineEdit(self.widget_2)
        self.password_line.setObjectName(u"password_line")
        self.password_line.setEchoMode(QLineEdit.EchoMode.PasswordEchoOnEdit)

        self.verticalLayout_3.addWidget(self.password_line)


        self.gridLayout_3.addWidget(self.widget_2, 3, 1, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 0, 1, 1, 1)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_3, 2, 1, 1, 1)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_5, 4, 1, 1, 1)


        self.verticalLayout.addWidget(self.widget_4)


        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.gridLayout_4 = QGridLayout(self.page_2)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.frame_2 = QFrame(self.page_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.widget = QWidget(self.frame_2)
        self.widget.setObjectName(u"widget")
        self.widget.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.logout_button = QPushButton(self.widget)
        self.logout_button.setObjectName(u"logout_button")

        self.horizontalLayout.addWidget(self.logout_button)


        self.verticalLayout_4.addWidget(self.widget)

        self.line = QFrame(self.frame_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.widget_5 = QWidget(self.frame_2)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_5 = QVBoxLayout(self.widget_5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.menu_tab = QTabWidget(self.widget_5)
        self.menu_tab.setObjectName(u"menu_tab")
        self.menu_tab.setTabPosition(QTabWidget.TabPosition.North)
        self.menu_tab.setTabShape(QTabWidget.TabShape.Rounded)
        self.menu_tab.setElideMode(Qt.TextElideMode.ElideMiddle)
        self.users = QWidget()
        self.users.setObjectName(u"users")
        self.menu_tab.addTab(self.users, "")
        self.INPUTS = QWidget()
        self.INPUTS.setObjectName(u"INPUTS")
        self.menu_tab.addTab(self.INPUTS, "")
        self.stations = QWidget()
        self.stations.setObjectName(u"stations")
        self.verticalLayout_8 = QVBoxLayout(self.stations)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.widget_9 = QWidget(self.stations)
        self.widget_9.setObjectName(u"widget_9")
        self.widget_9.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_4 = QHBoxLayout(self.widget_9)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_6)

        self.search_station_line = QLineEdit(self.widget_9)
        self.search_station_line.setObjectName(u"search_station_line")
        self.search_station_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_4.addWidget(self.search_station_line)

        self.search_station_button = QPushButton(self.widget_9)
        self.search_station_button.setObjectName(u"search_station_button")

        self.horizontalLayout_4.addWidget(self.search_station_button)

        self.line_7 = QFrame(self.widget_9)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_7)

        self.add_station_button = QPushButton(self.widget_9)
        self.add_station_button.setObjectName(u"add_station_button")

        self.horizontalLayout_4.addWidget(self.add_station_button)

        self.line_8 = QFrame(self.widget_9)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.VLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_8)

        self.refresh_stations_table_button = QPushButton(self.widget_9)
        self.refresh_stations_table_button.setObjectName(u"refresh_stations_table_button")

        self.horizontalLayout_4.addWidget(self.refresh_stations_table_button)


        self.verticalLayout_8.addWidget(self.widget_9)

        self.line_6 = QFrame(self.stations)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_8.addWidget(self.line_6)

        self.widget_10 = QWidget(self.stations)
        self.widget_10.setObjectName(u"widget_10")
        self.gridLayout_6 = QGridLayout(self.widget_10)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.stations_table = QTableWidget(self.widget_10)
        self.stations_table.setObjectName(u"stations_table")

        self.gridLayout_6.addWidget(self.stations_table, 0, 0, 1, 1)


        self.verticalLayout_8.addWidget(self.widget_10)

        self.menu_tab.addTab(self.stations, "")
        self.streams = QWidget()
        self.streams.setObjectName(u"streams")
        self.verticalLayout_7 = QVBoxLayout(self.streams)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_7 = QWidget(self.streams)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMaximumSize(QSize(16777215, 100))
        self.horizontalLayout_3 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.search_stream_line = QLineEdit(self.widget_7)
        self.search_stream_line.setObjectName(u"search_stream_line")
        self.search_stream_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_3.addWidget(self.search_stream_line)

        self.search_stream_button = QPushButton(self.widget_7)
        self.search_stream_button.setObjectName(u"search_stream_button")

        self.horizontalLayout_3.addWidget(self.search_stream_button)

        self.line_4 = QFrame(self.widget_7)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line_4)

        self.add_stream_button = QPushButton(self.widget_7)
        self.add_stream_button.setObjectName(u"add_stream_button")

        self.horizontalLayout_3.addWidget(self.add_stream_button)

        self.line_5 = QFrame(self.widget_7)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line_5)

        self.reload_streams_table_button = QPushButton(self.widget_7)
        self.reload_streams_table_button.setObjectName(u"reload_streams_table_button")

        self.horizontalLayout_3.addWidget(self.reload_streams_table_button)


        self.verticalLayout_7.addWidget(self.widget_7)

        self.line_3 = QFrame(self.streams)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_3)

        self.widget_8 = QWidget(self.streams)
        self.widget_8.setObjectName(u"widget_8")
        self.gridLayout_5 = QGridLayout(self.widget_8)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.streams_table = QTableWidget(self.widget_8)
        self.streams_table.setObjectName(u"streams_table")

        self.gridLayout_5.addWidget(self.streams_table, 0, 0, 1, 1)


        self.verticalLayout_7.addWidget(self.widget_8)

        self.menu_tab.addTab(self.streams, "")
        self.transmissions = QWidget()
        self.transmissions.setObjectName(u"transmissions")
        self.menu_tab.addTab(self.transmissions, "")
        self.SETTINGS = QWidget()
        self.SETTINGS.setObjectName(u"SETTINGS")
        self.verticalLayout_6 = QVBoxLayout(self.SETTINGS)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.widget_6 = QWidget(self.SETTINGS)
        self.widget_6.setObjectName(u"widget_6")
        self.horizontalLayout_2 = QHBoxLayout(self.widget_6)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_6 = QLabel(self.widget_6)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.theme_combo = QComboBox(self.widget_6)
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.addItem("")
        self.theme_combo.setObjectName(u"theme_combo")

        self.horizontalLayout_2.addWidget(self.theme_combo)


        self.verticalLayout_6.addWidget(self.widget_6)

        self.line_2 = QFrame(self.SETTINGS)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_6.addWidget(self.line_2)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_7)

        self.menu_tab.addTab(self.SETTINGS, "")

        self.verticalLayout_5.addWidget(self.menu_tab)


        self.verticalLayout_4.addWidget(self.widget_5)


        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_2)

        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 974, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(1)
        self.menu_tab.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"NEXTAI CAST", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:26pt;\">NEXTAI-CAST</span></p></body></html>", None))
        self.login_button.setText(QCoreApplication.translate("MainWindow", u"LOGIN", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:12pt;\">BY NEXTAI SOLUTIONS</span></p></body></html>", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">USERNAME</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt;\">PASSWORD</span></p></body></html>", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt;\">MENU</span></p></body></html>", None))
        self.logout_button.setText(QCoreApplication.translate("MainWindow", u"LOGOUT", None))
        self.menu_tab.setTabText(self.menu_tab.indexOf(self.users), QCoreApplication.translate("MainWindow", u"USERS", None))
        self.menu_tab.setTabText(self.menu_tab.indexOf(self.INPUTS), QCoreApplication.translate("MainWindow", u"INPUTS", None))
        self.search_station_line.setPlaceholderText(QCoreApplication.translate("MainWindow", u"STATION NAME HERE", None))
        self.search_station_button.setText(QCoreApplication.translate("MainWindow", u"SEARCH", None))
        self.add_station_button.setText(QCoreApplication.translate("MainWindow", u"ADD STATION", None))
        self.refresh_stations_table_button.setText(QCoreApplication.translate("MainWindow", u"REFRESH TABLE", None))
        self.menu_tab.setTabText(self.menu_tab.indexOf(self.stations), QCoreApplication.translate("MainWindow", u"STATIONS", None))
        self.search_stream_line.setPlaceholderText(QCoreApplication.translate("MainWindow", u"STREAM NAME HERE", None))
        self.search_stream_button.setText(QCoreApplication.translate("MainWindow", u"SEARCH", None))
        self.add_stream_button.setText(QCoreApplication.translate("MainWindow", u"ADD STREAM", None))
        self.reload_streams_table_button.setText(QCoreApplication.translate("MainWindow", u"RELOAD TABLE", None))
        self.menu_tab.setTabText(self.menu_tab.indexOf(self.streams), QCoreApplication.translate("MainWindow", u"STREAMS", None))
        self.menu_tab.setTabText(self.menu_tab.indexOf(self.transmissions), QCoreApplication.translate("MainWindow", u"TRANSMISSION", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\">SELECT APP THEME: </p></body></html>", None))
        self.theme_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"light_amber.xml", None))
        self.theme_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"light_blue.xml", None))
        self.theme_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"light_cyan.xml", None))
        self.theme_combo.setItemText(3, QCoreApplication.translate("MainWindow", u"light_cyan_500.xml", None))
        self.theme_combo.setItemText(4, QCoreApplication.translate("MainWindow", u"light_lightgreen.xml", None))
        self.theme_combo.setItemText(5, QCoreApplication.translate("MainWindow", u"light_pink.xml", None))
        self.theme_combo.setItemText(6, QCoreApplication.translate("MainWindow", u"light_purple.xml", None))
        self.theme_combo.setItemText(7, QCoreApplication.translate("MainWindow", u"light_red.xml", None))
        self.theme_combo.setItemText(8, QCoreApplication.translate("MainWindow", u"light_teal.xml", None))
        self.theme_combo.setItemText(9, QCoreApplication.translate("MainWindow", u"light_yellow.xml", None))
        self.theme_combo.setItemText(10, QCoreApplication.translate("MainWindow", u"dark_amber.xml", None))
        self.theme_combo.setItemText(11, QCoreApplication.translate("MainWindow", u"dark_blue.xml", None))
        self.theme_combo.setItemText(12, QCoreApplication.translate("MainWindow", u"dark_cyan.xml", None))
        self.theme_combo.setItemText(13, QCoreApplication.translate("MainWindow", u"dark_lightgreen.xml", None))
        self.theme_combo.setItemText(14, QCoreApplication.translate("MainWindow", u"dark_pink.xml", None))
        self.theme_combo.setItemText(15, QCoreApplication.translate("MainWindow", u"dark_purple.xml", None))
        self.theme_combo.setItemText(16, QCoreApplication.translate("MainWindow", u"dark_red.xml", None))
        self.theme_combo.setItemText(17, QCoreApplication.translate("MainWindow", u"dark_teal.xml", None))
        self.theme_combo.setItemText(18, QCoreApplication.translate("MainWindow", u"dark_yellow.xml", None))

        self.menu_tab.setTabText(self.menu_tab.indexOf(self.SETTINGS), QCoreApplication.translate("MainWindow", u"SETTINGS", None))
    # retranslateUi

