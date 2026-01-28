# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.10.1
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QSizePolicy, QStatusBar, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(980, 674)
        self.actionOpenImage = QAction(MainWindow)
        self.actionOpenImage.setObjectName(u"actionOpenImage")
        self.actionOpenBBDirectory = QAction(MainWindow)
        self.actionOpenBBDirectory.setObjectName(u"actionOpenBBDirectory")
        self.actionChooseCalibration = QAction(MainWindow)
        self.actionChooseCalibration.setObjectName(u"actionChooseCalibration")
        self.actionOpen_Other = QAction(MainWindow)
        self.actionOpen_Other.setObjectName(u"actionOpen_Other")
        self.actionView_Selected_Image = QAction(MainWindow)
        self.actionView_Selected_Image.setObjectName(u"actionView_Selected_Image")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(700, 580, 271, 51))
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 10, 201, 621))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelWorkspaceFiles = QLabel(self.layoutWidget)
        self.labelWorkspaceFiles.setObjectName(u"labelWorkspaceFiles")
        font = QFont()
        font.setPointSize(12)
        self.labelWorkspaceFiles.setFont(font)
        self.labelWorkspaceFiles.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.labelWorkspaceFiles)

        self.widgetWorkspaceList = QListWidget(self.layoutWidget)
        self.widgetWorkspaceList.setObjectName(u"widgetWorkspaceList")
        font1 = QFont()
        font1.setPointSize(7)
        self.widgetWorkspaceList.setFont(font1)

        self.verticalLayout.addWidget(self.widgetWorkspaceList)

        self.imagelabel = QLabel(self.centralwidget)
        self.imagelabel.setObjectName(u"imagelabel")
        self.imagelabel.setGeometry(QRect(250, 20, 711, 551))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 980, 19))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName(u"menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName(u"menuView")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addAction(self.actionOpenBBDirectory)
        self.menuFile.addAction(self.actionOpen_Other)
        self.menuEdit.addAction(self.actionChooseCalibration)
        self.menuView.addAction(self.actionView_Selected_Image)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpenImage.setText(QCoreApplication.translate("MainWindow", u"Open Image", None))
        self.actionOpenBBDirectory.setText(QCoreApplication.translate("MainWindow", u"Open Directory", None))
        self.actionChooseCalibration.setText(QCoreApplication.translate("MainWindow", u"Calibration", None))
        self.actionOpen_Other.setText(QCoreApplication.translate("MainWindow", u"Open Other", None))
        self.actionView_Selected_Image.setText(QCoreApplication.translate("MainWindow", u"View Selected Image", None))
        self.labelWorkspaceFiles.setText(QCoreApplication.translate("MainWindow", u"Workspace Files", None))
        self.imagelabel.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", u"View", None))
    # retranslateUi

