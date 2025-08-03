# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_Window.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QStatusBar, QTabWidget, QToolButton,
    QWidget)

class Ui_Main_Windows(object):
    def setupUi(self, Main_Windows):
        if not Main_Windows.objectName():
            Main_Windows.setObjectName(u"Main_Windows")
        Main_Windows.setEnabled(True)
        Main_Windows.resize(738, 790)
        Main_Windows.setMinimumSize(QSize(0, 0))
        font = QFont()
        font.setPointSize(9)
        Main_Windows.setFont(font)
        Main_Windows.setAcceptDrops(True)
        Main_Windows.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        Main_Windows.setAnimated(True)
        Main_Windows.setDocumentMode(False)
        Main_Windows.setTabShape(QTabWidget.TabShape.Rounded)
        self.centralwidget = QWidget(Main_Windows)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        font1 = QFont()
        font1.setPointSize(9)
        font1.setBold(False)
        font1.setStrikeOut(False)
        self.centralwidget.setFont(font1)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.verticalSpacer = QSpacerItem(20, 7, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)

        self.gridLayout.addItem(self.verticalSpacer, 3, 1, 1, 1)

        self.horizontalLayout_bottom = QHBoxLayout()
        self.horizontalLayout_bottom.setObjectName(u"horizontalLayout_bottom")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_bottom.addItem(self.horizontalSpacer)

        self.Check_Button = QPushButton(self.centralwidget)
        self.Check_Button.setObjectName(u"Check_Button")
        self.Check_Button.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.Check_Button.sizePolicy().hasHeightForWidth())
        self.Check_Button.setSizePolicy(sizePolicy1)
        self.Check_Button.setMinimumSize(QSize(130, 60))
        self.Check_Button.setMaximumSize(QSize(250, 110))
        font2 = QFont()
        font2.setPointSize(25)
        font2.setBold(True)
        font2.setStrikeOut(False)
        self.Check_Button.setFont(font2)
        self.Check_Button.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.horizontalLayout_bottom.addWidget(self.Check_Button, 0, Qt.AlignmentFlag.AlignVCenter)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_bottom.addItem(self.horizontalSpacer_2)


        self.gridLayout.addLayout(self.horizontalLayout_bottom, 4, 0, 1, 3)

        self.gridLayout_top = QGridLayout()
        self.gridLayout_top.setObjectName(u"gridLayout_top")
        self.horizontalSpacer_3 = QSpacerItem(40, 0, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.gridLayout_top.addItem(self.horizontalSpacer_3, 1, 0, 1, 1)

        self.Form_Title = QLabel(self.centralwidget)
        self.Form_Title.setObjectName(u"Form_Title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.Form_Title.sizePolicy().hasHeightForWidth())
        self.Form_Title.setSizePolicy(sizePolicy2)
        self.Form_Title.setMinimumSize(QSize(400, 80))
        font3 = QFont()
        font3.setFamilies([u"Bahnschrift"])
        font3.setPointSize(60)
        font3.setBold(True)
        font3.setStrikeOut(False)
        font3.setKerning(True)
        self.Form_Title.setFont(font3)
        self.Form_Title.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.Form_Title.setTextFormat(Qt.TextFormat.MarkdownText)
        self.Form_Title.setScaledContents(False)
        self.Form_Title.setAlignment(Qt.AlignmentFlag.AlignBottom|Qt.AlignmentFlag.AlignHCenter)

        self.gridLayout_top.addWidget(self.Form_Title, 2, 0, 1, 3)

        self.Form_Select = QToolButton(self.centralwidget)
        self.Form_Select.setObjectName(u"Form_Select")
        font4 = QFont()
        font4.setPointSize(13)
        font4.setBold(False)
        font4.setStrikeOut(False)
        self.Form_Select.setFont(font4)

        self.gridLayout_top.addWidget(self.Form_Select, 1, 1, 1, 1, Qt.AlignmentFlag.AlignTop)

        self.Settings_Button = QPushButton(self.centralwidget)
        self.Settings_Button.setObjectName(u"Settings_Button")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.Settings_Button.sizePolicy().hasHeightForWidth())
        self.Settings_Button.setSizePolicy(sizePolicy3)
        self.Settings_Button.setMinimumSize(QSize(60, 60))

        self.gridLayout_top.addWidget(self.Settings_Button, 1, 2, 1, 1)


        self.gridLayout.addLayout(self.gridLayout_top, 0, 0, 1, 3)

        self.Table_Scroll_Area = QScrollArea(self.centralwidget)
        self.Table_Scroll_Area.setObjectName(u"Table_Scroll_Area")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.Table_Scroll_Area.sizePolicy().hasHeightForWidth())
        self.Table_Scroll_Area.setSizePolicy(sizePolicy4)
        self.Table_Scroll_Area.setMinimumSize(QSize(300, 300))
        self.Table_Scroll_Area.setWidgetResizable(True)
        self.Scroll_Area_Widget_Contents = QWidget()
        self.Scroll_Area_Widget_Contents.setObjectName(u"Scroll_Area_Widget_Contents")
        self.Scroll_Area_Widget_Contents.setGeometry(QRect(0, 0, 718, 498))
        sizePolicy.setHeightForWidth(self.Scroll_Area_Widget_Contents.sizePolicy().hasHeightForWidth())
        self.Scroll_Area_Widget_Contents.setSizePolicy(sizePolicy)
        self.Table_Scroll_Area.setWidget(self.Scroll_Area_Widget_Contents)

        self.gridLayout.addWidget(self.Table_Scroll_Area, 2, 0, 1, 3)

        Main_Windows.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(Main_Windows)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setEnabled(True)
        self.statusbar.setFont(font)
        Main_Windows.setStatusBar(self.statusbar)

        self.retranslateUi(Main_Windows)

        QMetaObject.connectSlotsByName(Main_Windows)
    # setupUi

    def retranslateUi(self, Main_Windows):
        Main_Windows.setWindowTitle(QCoreApplication.translate("Main_Windows", u"Latein Formen Trainer", None))
        self.Check_Button.setText(QCoreApplication.translate("Main_Windows", u"check", None))
        self.Form_Title.setText(QCoreApplication.translate("Main_Windows", u"Form Title", None))
        self.Form_Select.setText(QCoreApplication.translate("Main_Windows", u"Select Form", None))
        self.Settings_Button.setText("")
    # retranslateUi

