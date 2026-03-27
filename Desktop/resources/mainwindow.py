# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QStatusBar, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(989, 638)
        self.light_amber = QAction(MainWindow)
        self.light_amber.setObjectName(u"light_amber")
        self.light_blue = QAction(MainWindow)
        self.light_blue.setObjectName(u"light_blue")
        self.light_cyan = QAction(MainWindow)
        self.light_cyan.setObjectName(u"light_cyan")
        self.light_cyan_500 = QAction(MainWindow)
        self.light_cyan_500.setObjectName(u"light_cyan_500")
        self.light_green = QAction(MainWindow)
        self.light_green.setObjectName(u"light_green")
        self.light_pink = QAction(MainWindow)
        self.light_pink.setObjectName(u"light_pink")
        self.light_purple = QAction(MainWindow)
        self.light_purple.setObjectName(u"light_purple")
        self.light_red = QAction(MainWindow)
        self.light_red.setObjectName(u"light_red")
        self.light_teal = QAction(MainWindow)
        self.light_teal.setObjectName(u"light_teal")
        self.light_yellow = QAction(MainWindow)
        self.light_yellow.setObjectName(u"light_yellow")
        self.dark_amber = QAction(MainWindow)
        self.dark_amber.setObjectName(u"dark_amber")
        self.dark_blue = QAction(MainWindow)
        self.dark_blue.setObjectName(u"dark_blue")
        self.dark_cyan = QAction(MainWindow)
        self.dark_cyan.setObjectName(u"dark_cyan")
        self.dark_green = QAction(MainWindow)
        self.dark_green.setObjectName(u"dark_green")
        self.dark_pink = QAction(MainWindow)
        self.dark_pink.setObjectName(u"dark_pink")
        self.dark_purple = QAction(MainWindow)
        self.dark_purple.setObjectName(u"dark_purple")
        self.dark_red = QAction(MainWindow)
        self.dark_red.setObjectName(u"dark_red")
        self.dark_teal = QAction(MainWindow)
        self.dark_teal.setObjectName(u"dark_teal")
        self.dark_yellow = QAction(MainWindow)
        self.dark_yellow.setObjectName(u"dark_yellow")
        self.actionVIEW_USRS_DATA = QAction(MainWindow)
        self.actionVIEW_USRS_DATA.setObjectName(u"actionVIEW_USRS_DATA")
        self.manage_users = QAction(MainWindow)
        self.manage_users.setObjectName(u"manage_users")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.stackedWidget = QStackedWidget(self.widget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.gridLayout_3 = QGridLayout(self.page)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.frame_2 = QFrame(self.page)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(350, 500))
        self.frame_2.setStyleSheet(u"")
        self.frame_2.setFrameShape(QFrame.Shape.Box)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.frame_2.setLineWidth(5)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.widget1 = QWidget(self.frame_2)
        self.widget1.setObjectName(u"widget1")
        self.verticalLayout_4 = QVBoxLayout(self.widget1)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.label_4 = QLabel(self.widget1)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.label_4)


        self.verticalLayout.addWidget(self.widget1)

        self.verticalSpacer_5 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_5)

        self.widget_2 = QWidget(self.frame_2)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.username_lineEdit = QLineEdit(self.widget_2)
        self.username_lineEdit.setObjectName(u"username_lineEdit")

        self.verticalLayout_2.addWidget(self.username_lineEdit)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_2.addItem(self.verticalSpacer_4)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.password_lineEdit = QLineEdit(self.widget_2)
        self.password_lineEdit.setObjectName(u"password_lineEdit")
        self.password_lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.verticalLayout_2.addWidget(self.password_lineEdit)


        self.verticalLayout.addWidget(self.widget_2)

        self.verticalSpacer_6 = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_6)

        self.widget_3 = QWidget(self.frame_2)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_3 = QVBoxLayout(self.widget_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.label_3)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.sing_in_pushButton = QPushButton(self.widget_3)
        self.sing_in_pushButton.setObjectName(u"sing_in_pushButton")
        self.sing_in_pushButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout_3.addWidget(self.sing_in_pushButton)


        self.verticalLayout.addWidget(self.widget_3)


        self.gridLayout_3.addWidget(self.frame_2, 1, 1, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 0, 1, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer_2, 1, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_3.addItem(self.horizontalSpacer, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_7 = QVBoxLayout(self.page_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.widget_4 = QWidget(self.page_2)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout = QHBoxLayout(self.widget_4)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(self.widget_4)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.logout_button = QPushButton(self.widget_4)
        self.logout_button.setObjectName(u"logout_button")

        self.horizontalLayout.addWidget(self.logout_button)


        self.verticalLayout_7.addWidget(self.widget_4)

        self.line = QFrame(self.page_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.widget_5 = QWidget(self.page_2)
        self.widget_5.setObjectName(u"widget_5")
        self.verticalLayout_6 = QVBoxLayout(self.widget_5)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")

        self.verticalLayout_7.addWidget(self.widget_5)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_5 = QVBoxLayout(self.page_3)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widget_7 = QWidget(self.page_3)
        self.widget_7.setObjectName(u"widget_7")
        self.widget_7.setMaximumSize(QSize(16777215, 50))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_7)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_5 = QLabel(self.widget_7)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.label_5)

        self.horizontalSpacer_4 = QSpacerItem(100, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.users_search_line = QLineEdit(self.widget_7)
        self.users_search_line.setObjectName(u"users_search_line")
        self.users_search_line.setMaximumSize(QSize(200, 16777215))
        self.users_search_line.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.users_search_line)

        self.users_search_button = QPushButton(self.widget_7)
        self.users_search_button.setObjectName(u"users_search_button")

        self.horizontalLayout_2.addWidget(self.users_search_button)

        self.line_5 = QFrame(self.widget_7)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_5)

        self.users_role_combo = QComboBox(self.widget_7)
        self.users_role_combo.addItem("")
        self.users_role_combo.addItem("")
        self.users_role_combo.addItem("")
        self.users_role_combo.setObjectName(u"users_role_combo")

        self.horizontalLayout_2.addWidget(self.users_role_combo)

        self.line_4 = QFrame(self.widget_7)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_4)

        self.users_create_button = QPushButton(self.widget_7)
        self.users_create_button.setObjectName(u"users_create_button")

        self.horizontalLayout_2.addWidget(self.users_create_button)

        self.line_3 = QFrame(self.widget_7)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.VLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_3)

        self.users_return_button = QPushButton(self.widget_7)
        self.users_return_button.setObjectName(u"users_return_button")

        self.horizontalLayout_2.addWidget(self.users_return_button)


        self.verticalLayout_5.addWidget(self.widget_7)

        self.line_2 = QFrame(self.page_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_5.addWidget(self.line_2)

        self.widget_6 = QWidget(self.page_3)
        self.widget_6.setObjectName(u"widget_6")
        self.gridLayout_4 = QGridLayout(self.widget_6)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.users_table = QTableWidget(self.widget_6)
        self.users_table.setObjectName(u"users_table")
        self.users_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

        self.gridLayout_4.addWidget(self.users_table, 0, 0, 1, 1)


        self.verticalLayout_5.addWidget(self.widget_6)

        self.stackedWidget.addWidget(self.page_3)

        self.gridLayout_2.addWidget(self.stackedWidget, 0, 0, 1, 1)


        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 989, 33))
        self.device_inputs_menu = QMenu(self.menubar)
        self.device_inputs_menu.setObjectName(u"device_inputs_menu")
        self.stream_inputs_menu = QMenu(self.menubar)
        self.stream_inputs_menu.setObjectName(u"stream_inputs_menu")
        self.users_menu = QMenu(self.menubar)
        self.users_menu.setObjectName(u"users_menu")
        self.stations_menu = QMenu(self.menubar)
        self.stations_menu.setObjectName(u"stations_menu")
        self.streams_menu = QMenu(self.menubar)
        self.streams_menu.setObjectName(u"streams_menu")
        self.transmissions_menu = QMenu(self.menubar)
        self.transmissions_menu.setObjectName(u"transmissions_menu")
        self.menuTHEME = QMenu(self.menubar)
        self.menuTHEME.setObjectName(u"menuTHEME")
        self.menuLIGHT_THEMES = QMenu(self.menuTHEME)
        self.menuLIGHT_THEMES.setObjectName(u"menuLIGHT_THEMES")
        self.menuDARK_THEMES = QMenu(self.menuTHEME)
        self.menuDARK_THEMES.setObjectName(u"menuDARK_THEMES")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.users_menu.menuAction())
        self.menubar.addAction(self.stream_inputs_menu.menuAction())
        self.menubar.addAction(self.device_inputs_menu.menuAction())
        self.menubar.addAction(self.stations_menu.menuAction())
        self.menubar.addAction(self.streams_menu.menuAction())
        self.menubar.addAction(self.transmissions_menu.menuAction())
        self.menubar.addAction(self.menuTHEME.menuAction())
        self.users_menu.addAction(self.manage_users)
        self.menuTHEME.addAction(self.menuLIGHT_THEMES.menuAction())
        self.menuTHEME.addSeparator()
        self.menuTHEME.addAction(self.menuDARK_THEMES.menuAction())
        self.menuTHEME.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_amber)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_blue)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_cyan)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_cyan_500)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_green)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_pink)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_purple)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_red)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_teal)
        self.menuLIGHT_THEMES.addSeparator()
        self.menuLIGHT_THEMES.addAction(self.light_yellow)
        self.menuDARK_THEMES.addAction(self.dark_amber)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_blue)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_cyan)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_green)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_pink)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_purple)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_red)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_teal)
        self.menuDARK_THEMES.addSeparator()
        self.menuDARK_THEMES.addAction(self.dark_yellow)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"NEXTAI CAST", None))
        self.light_amber.setText(QCoreApplication.translate("MainWindow", u"AMBER", None))
        self.light_blue.setText(QCoreApplication.translate("MainWindow", u"BLUE", None))
        self.light_cyan.setText(QCoreApplication.translate("MainWindow", u"CYAN", None))
        self.light_cyan_500.setText(QCoreApplication.translate("MainWindow", u"CYAN 500", None))
        self.light_green.setText(QCoreApplication.translate("MainWindow", u"GREEN", None))
        self.light_pink.setText(QCoreApplication.translate("MainWindow", u"PINK", None))
        self.light_purple.setText(QCoreApplication.translate("MainWindow", u"PURPLE", None))
        self.light_red.setText(QCoreApplication.translate("MainWindow", u"RED", None))
        self.light_teal.setText(QCoreApplication.translate("MainWindow", u"TEAL", None))
        self.light_yellow.setText(QCoreApplication.translate("MainWindow", u"YELLOW", None))
        self.dark_amber.setText(QCoreApplication.translate("MainWindow", u"AMBER", None))
        self.dark_blue.setText(QCoreApplication.translate("MainWindow", u"BLUE", None))
        self.dark_cyan.setText(QCoreApplication.translate("MainWindow", u"CYAN", None))
        self.dark_green.setText(QCoreApplication.translate("MainWindow", u"GREEN", None))
        self.dark_pink.setText(QCoreApplication.translate("MainWindow", u"PINK", None))
        self.dark_purple.setText(QCoreApplication.translate("MainWindow", u"PURPLE", None))
        self.dark_red.setText(QCoreApplication.translate("MainWindow", u"RED", None))
        self.dark_teal.setText(QCoreApplication.translate("MainWindow", u"TEAL", None))
        self.dark_yellow.setText(QCoreApplication.translate("MainWindow", u"YELLOW", None))
        self.actionVIEW_USRS_DATA.setText(QCoreApplication.translate("MainWindow", u"VIEW USRS DATA", None))
        self.manage_users.setText(QCoreApplication.translate("MainWindow", u"Manage Users", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:24pt; font-weight:700;\">NEXTAI CAST</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">Username</span></p></body></html>", None))
        self.username_lineEdit.setInputMask("")
        self.username_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"username here", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">Password</span></p></body></html>", None))
        self.password_lineEdit.setInputMask("")
        self.password_lineEdit.setPlaceholderText(QCoreApplication.translate("MainWindow", u"password here", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">By NextAI Solutions</span></p></body></html>", None))
        self.sing_in_pushButton.setText(QCoreApplication.translate("MainWindow", u"Sing In", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">MENU PRINCIPAL</span></p></body></html>", None))
        self.logout_button.setText(QCoreApplication.translate("MainWindow", u"LOGOUT", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:14pt; font-weight:700;\">MANAGE USERS</span></p></body></html>", None))
        self.users_search_button.setText(QCoreApplication.translate("MainWindow", u"SEARCH", None))
        self.users_role_combo.setItemText(0, QCoreApplication.translate("MainWindow", u"ALL", None))
        self.users_role_combo.setItemText(1, QCoreApplication.translate("MainWindow", u"ADMINS", None))
        self.users_role_combo.setItemText(2, QCoreApplication.translate("MainWindow", u"USERS", None))

        self.users_role_combo.setCurrentText(QCoreApplication.translate("MainWindow", u"ALL", None))
        self.users_role_combo.setPlaceholderText(QCoreApplication.translate("MainWindow", u"ROLE", None))
        self.users_create_button.setText(QCoreApplication.translate("MainWindow", u"+ CREATE USER", None))
        self.users_return_button.setText(QCoreApplication.translate("MainWindow", u"RETURN", None))
        self.device_inputs_menu.setTitle(QCoreApplication.translate("MainWindow", u"DEVICE INPUTS", None))
        self.stream_inputs_menu.setTitle(QCoreApplication.translate("MainWindow", u"STREAM INPUTS", None))
        self.users_menu.setTitle(QCoreApplication.translate("MainWindow", u"USERS", None))
        self.stations_menu.setTitle(QCoreApplication.translate("MainWindow", u"STATIONS", None))
        self.streams_menu.setTitle(QCoreApplication.translate("MainWindow", u"STREAMS", None))
        self.transmissions_menu.setTitle(QCoreApplication.translate("MainWindow", u"TRANSMISSION", None))
        self.menuTHEME.setTitle(QCoreApplication.translate("MainWindow", u"THEMES", None))
        self.menuLIGHT_THEMES.setTitle(QCoreApplication.translate("MainWindow", u"LIGHT THEMES", None))
        self.menuDARK_THEMES.setTitle(QCoreApplication.translate("MainWindow", u"DARK THEMES", None))
    # retranslateUi

