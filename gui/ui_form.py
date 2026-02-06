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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QProgressBar,
    QPushButton, QSizePolicy, QSlider, QSpacerItem,
    QStatusBar, QTabWidget, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

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
        self.actionOpen_Project = QAction(MainWindow)
        self.actionOpen_Project.setObjectName(u"actionOpen_Project")
        self.actionSave_Project = QAction(MainWindow)
        self.actionSave_Project.setObjectName(u"actionSave_Project")
        self.actionNew_Project = QAction(MainWindow)
        self.actionNew_Project.setObjectName(u"actionNew_Project")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(10, 650, 1081, 31))
        self.progressBar.setValue(0)
        self.progressBar.setInvertedAppearance(False)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QRect(220, 0, 881, 641))
        self.imageTab = QWidget()
        self.imageTab.setObjectName(u"imageTab")
        self.imageTab.setEnabled(True)
        self.verticalLayoutWidget = QWidget(self.imageTab)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 871, 611))
        self.imageTabLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.imageTabLayout.setObjectName(u"imageTabLayout")
        self.imageTabLayout.setContentsMargins(0, 0, 0, 0)
        self.imagelabel = QLabel(self.verticalLayoutWidget)
        self.imagelabel.setObjectName(u"imagelabel")
        self.imagelabel.setMinimumSize(QSize(720, 480))
        self.imagelabel.setAlignment(Qt.AlignCenter)

        self.imageTabLayout.addWidget(self.imagelabel)

        self.imageTabVSpacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.imageTabLayout.addItem(self.imageTabVSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.priorFrame = QPushButton(self.verticalLayoutWidget)
        self.priorFrame.setObjectName(u"priorFrame")

        self.horizontalLayout.addWidget(self.priorFrame)

        self.frameSelection = QSlider(self.verticalLayoutWidget)
        self.frameSelection.setObjectName(u"frameSelection")
        self.frameSelection.setMinimumSize(QSize(0, 50))
        self.frameSelection.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.frameSelection)

        self.nextFrame = QPushButton(self.verticalLayoutWidget)
        self.nextFrame.setObjectName(u"nextFrame")

        self.horizontalLayout.addWidget(self.nextFrame)

        self.saveImage = QPushButton(self.verticalLayoutWidget)
        self.saveImage.setObjectName(u"saveImage")

        self.horizontalLayout.addWidget(self.saveImage)


        self.imageTabLayout.addLayout(self.horizontalLayout)

        self.tabWidget.addTab(self.imageTab, "")
        self.calTab = QWidget()
        self.calTab.setObjectName(u"calTab")
        self.calTab.setEnabled(True)
        self.verticalLayoutWidget_2 = QWidget(self.calTab)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(0, 0, 871, 611))
        self.calTabLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.calTabLayout.setObjectName(u"calTabLayout")
        self.calTabLayout.setContentsMargins(0, 0, 0, 0)
        self.labelCaliFigs = QLabel(self.verticalLayoutWidget_2)
        self.labelCaliFigs.setObjectName(u"labelCaliFigs")
        self.labelCaliFigs.setMinimumSize(QSize(0, 500))

        self.calTabLayout.addWidget(self.labelCaliFigs)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.calTabLayout.addItem(self.verticalSpacer)

        self.SavePlot = QPushButton(self.verticalLayoutWidget_2)
        self.SavePlot.setObjectName(u"SavePlot")

        self.calTabLayout.addWidget(self.SavePlot)

        self.tabWidget.addTab(self.calTab, "")
        self.nedtTab = QWidget()
        self.nedtTab.setObjectName(u"nedtTab")
        self.nedtTab.setEnabled(True)
        self.tabWidget.addTab(self.nedtTab, "")
        self.stabilityTab = QWidget()
        self.stabilityTab.setObjectName(u"stabilityTab")
        self.stabilityTab.setEnabled(True)
        self.tabWidget.addTab(self.stabilityTab, "")
        self.layoutWidget = QWidget(self.centralwidget)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 0, 201, 641))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.labelProjectFiles = QLabel(self.layoutWidget)
        self.labelProjectFiles.setObjectName(u"labelProjectFiles")
        font = QFont()
        font.setPointSize(12)
        self.labelProjectFiles.setFont(font)
        self.labelProjectFiles.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.labelProjectFiles)

        self.widgetProjectTreeList = QTreeWidget(self.layoutWidget)
        QTreeWidgetItem(self.widgetProjectTreeList)
        QTreeWidgetItem(self.widgetProjectTreeList)
        self.widgetProjectTreeList.setObjectName(u"widgetProjectTreeList")

        self.verticalLayout.addWidget(self.widgetProjectTreeList)

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
        self.menuFile.addAction(self.actionOpen_Project)
        self.menuFile.addAction(self.actionSave_Project)
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addSeparator()
        self.menuWorkflow.addAction(self.actionOpenBBDirectory)
        self.menuWorkflow.addAction(self.actionOpenImage)
        self.menuWorkflow.addAction(self.actionOpenOther)
        self.menuWorkflow.addSeparator()

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
        self.actionOpen_Project.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
        self.actionSave_Project.setText(QCoreApplication.translate("MainWindow", u"Open Project", None))
        self.actionNew_Project.setText(QCoreApplication.translate("MainWindow", u"Save Project", None))
        self.imagelabel.setText("")
        self.priorFrame.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.nextFrame.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.saveImage.setText(QCoreApplication.translate("MainWindow", u"Save Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.imageTab), QCoreApplication.translate("MainWindow", u"Image Preview", None))
        self.labelCaliFigs.setText(QCoreApplication.translate("MainWindow", u"TextLabel", None))
        self.SavePlot.setText(QCoreApplication.translate("MainWindow", u"Save Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.calTab), QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.nedtTab), QCoreApplication.translate("MainWindow", u"NEDT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stabilityTab), QCoreApplication.translate("MainWindow", u"Stability", None))
        self.labelProjectFiles.setText(QCoreApplication.translate("MainWindow", u"Project Files", None))
        ___qtreewidgetitem = self.widgetProjectTreeList.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("MainWindow", u"Current Project", None));

        __sortingEnabled = self.widgetProjectTreeList.isSortingEnabled()
        self.widgetProjectTreeList.setSortingEnabled(False)
        ___qtreewidgetitem1 = self.widgetProjectTreeList.topLevelItem(0)
        ___qtreewidgetitem1.setText(0, QCoreApplication.translate("MainWindow", u"Project Files", None));
        ___qtreewidgetitem2 = self.widgetProjectTreeList.topLevelItem(1)
        ___qtreewidgetitem2.setText(0, QCoreApplication.translate("MainWindow", u"Project Variables", None));
        self.widgetProjectTreeList.setSortingEnabled(__sortingEnabled)

        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuWorkflow.setTitle(QCoreApplication.translate("MainWindow", u"Workflow", None))
    # retranslateUi

