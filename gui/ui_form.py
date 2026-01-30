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
    QSizePolicy, QStatusBar, QTabWidget, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1097, 730)
        self.actionOpenImage = QAction(MainWindow)
        self.actionOpenImage.setObjectName(u"actionOpenImage")
        self.actionOpenBBDirectory = QAction(MainWindow)
        self.actionOpenBBDirectory.setObjectName(u"actionOpenBBDirectory")
        self.actionChooseCalibration = QAction(MainWindow)
        self.actionChooseCalibration.setObjectName(u"actionChooseCalibration")
        self.actionOpenOther = QAction(MainWindow)
        self.actionOpenOther.setObjectName(u"actionOpenOther")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 650, 1081, 31))
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 0, 201, 641))
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

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QRect(220, 0, 881, 641))
        self.imageTab = QWidget()
        self.imageTab.setObjectName(u"imageTab")
        self.imageTab.setEnabled(True)
        self.verticalLayoutWidget = QWidget(self.imageTab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(-1, -1, 871, 611))
        self.imageTabLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.imageTabLayout.setObjectName(u"imageTabLayout")
        self.imageTabLayout.setContentsMargins(0, 0, 0, 0)
        self.imagelabel = QLabel(self.imageTab)
        self.imagelabel.setObjectName(u"imagelabel")
        self.imagelabel.setGeometry(QRect(10, 10, 861, 581))
        self.imagelabel.setAlignment(Qt.AlignCenter)
        self.tabWidget.addTab(self.imageTab, "")
        self.calTab = QWidget()
        self.calTab.setObjectName(u"calTab")
        self.calTab.setEnabled(True)
        self.tabWidget.addTab(self.calTab, "")
        self.nedtTab = QWidget()
        self.nedtTab.setObjectName(u"nedtTab")
        self.nedtTab.setEnabled(True)
        self.tabWidget.addTab(self.nedtTab, "")
        self.stabilityTab = QWidget()
        self.stabilityTab.setObjectName(u"stabilityTab")
        self.stabilityTab.setEnabled(True)
        self.tabWidget.addTab(self.stabilityTab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.tabWidget.raise_()
        self.progressBar.raise_()
        self.layoutWidget.raise_()
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1097, 19))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuWorkflow = QMenu(self.menubar)
        self.menuWorkflow.setObjectName(u"menuWorkflow")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuWorkflow.menuAction())
        self.menuFile.addAction(self.actionOpenImage)
        self.menuFile.addAction(self.actionOpenOther)
        self.menuWorkflow.addAction(self.actionOpenBBDirectory)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionOpenImage.setText(QCoreApplication.translate("MainWindow", u"Open Image", None))
        self.actionOpenBBDirectory.setText(QCoreApplication.translate("MainWindow", u"Open Directory", None))
        self.actionChooseCalibration.setText(QCoreApplication.translate("MainWindow", u"Calibration", None))
        self.actionOpenOther.setText(QCoreApplication.translate("MainWindow", u"Open Other", None))
        self.labelWorkspaceFiles.setText(QCoreApplication.translate("MainWindow", u"Workspace Files", None))
        self.imagelabel.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.imageTab), QCoreApplication.translate("MainWindow", u"Image Preview", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.calTab), QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.nedtTab), QCoreApplication.translate("MainWindow", u"NEDT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stabilityTab), QCoreApplication.translate("MainWindow", u"Stability", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuWorkflow.setTitle(QCoreApplication.translate("MainWindow", u"Workflow", None))
    # retranslateUi

