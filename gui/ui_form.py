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
    QLayout, QMainWindow, QMenu, QMenuBar,
    QPlainTextEdit, QProgressBar, QPushButton, QSizePolicy,
    QSlider, QSpacerItem, QStatusBar, QTabWidget,
    QTextEdit, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1438, 846)
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.WindowText, brush)
        brush1 = QBrush(QColor(198, 198, 198, 255))
        brush1.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Button, brush1)
        brush2 = QBrush(QColor(255, 255, 255, 255))
        brush2.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Light, brush2)
        brush3 = QBrush(QColor(226, 226, 226, 255))
        brush3.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Midlight, brush3)
        brush4 = QBrush(QColor(99, 99, 99, 255))
        brush4.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Dark, brush4)
        brush5 = QBrush(QColor(132, 132, 132, 255))
        brush5.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.BrightText, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Base, brush2)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Shadow, brush)
        brush6 = QBrush(QColor(85, 85, 255, 255))
        brush6.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Highlight, brush6)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.AlternateBase, brush3)
        brush7 = QBrush(QColor(255, 255, 220, 255))
        brush7.setStyle(Qt.BrushStyle.SolidPattern)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipBase, brush7)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.ToolTipText, brush)
        brush8 = QBrush(QColor(0, 0, 0, 127))
        brush8.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.PlaceholderText, brush8)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Active, QPalette.ColorRole.Accent, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.WindowText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Midlight, brush3)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.BrightText, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ButtonText, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, brush2)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Shadow, brush)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Highlight, brush6)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.AlternateBase, brush3)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipBase, brush7)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.ToolTipText, brush)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.PlaceholderText, brush8)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Inactive, QPalette.ColorRole.Accent, brush2)
#endif
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Light, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Midlight, brush3)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Dark, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Mid, brush5)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.BrightText, brush2)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, brush4)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Window, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Shadow, brush)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.AlternateBase, brush1)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipBase, brush7)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ToolTipText, brush)
        brush9 = QBrush(QColor(99, 99, 99, 127))
        brush9.setStyle(Qt.BrushStyle.SolidPattern)
#if QT_VERSION >= QT_VERSION_CHECK(5, 12, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.PlaceholderText, brush9)
#endif
#if QT_VERSION >= QT_VERSION_CHECK(6, 6, 0)
        palette.setBrush(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Accent, brush2)
#endif
        MainWindow.setPalette(palette)
        icon = QIcon(QIcon.fromTheme(u"applications-engineering"))
        MainWindow.setWindowIcon(icon)
        MainWindow.setWindowOpacity(1.000000000000000)
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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(1200, 800))
        self.centralwidget.setMaximumSize(QSize(64000, 64000))
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainHorzLayout = QHBoxLayout()
        self.mainHorzLayout.setObjectName(u"mainHorzLayout")
        self.mainHorzLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.projectVertLayout = QVBoxLayout()
        self.projectVertLayout.setObjectName(u"projectVertLayout")
        self.labelProjectFiles = QLabel(self.centralwidget)
        self.labelProjectFiles.setObjectName(u"labelProjectFiles")
        self.labelProjectFiles.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.labelProjectFiles.sizePolicy().hasHeightForWidth())
        self.labelProjectFiles.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(12)
        self.labelProjectFiles.setFont(font)
        self.labelProjectFiles.setAlignment(Qt.AlignCenter)

        self.projectVertLayout.addWidget(self.labelProjectFiles)

        self.widgetProjectTreeList = QTreeWidget(self.centralwidget)
        QTreeWidgetItem(self.widgetProjectTreeList)
        QTreeWidgetItem(self.widgetProjectTreeList)
        self.widgetProjectTreeList.setObjectName(u"widgetProjectTreeList")
        sizePolicy1.setHeightForWidth(self.widgetProjectTreeList.sizePolicy().hasHeightForWidth())
        self.widgetProjectTreeList.setSizePolicy(sizePolicy1)
        self.widgetProjectTreeList.setMaximumSize(QSize(250, 1000))

        self.projectVertLayout.addWidget(self.widgetProjectTreeList)


        self.mainHorzLayout.addLayout(self.projectVertLayout)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setEnabled(True)
        self.tabWidget.setMinimumSize(QSize(900, 600))
        self.imageTab = QWidget()
        self.imageTab.setObjectName(u"imageTab")
        self.imageTab.setEnabled(True)
        sizePolicy.setHeightForWidth(self.imageTab.sizePolicy().hasHeightForWidth())
        self.imageTab.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.imageTab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.imageTabLayout = QVBoxLayout()
        self.imageTabLayout.setObjectName(u"imageTabLayout")
        self.imagelabel = QLabel(self.imageTab)
        self.imagelabel.setObjectName(u"imagelabel")
        self.imagelabel.setMinimumSize(QSize(720, 600))
        self.imagelabel.setAlignment(Qt.AlignCenter)

        self.imageTabLayout.addWidget(self.imagelabel)

        self.imageTabVSpacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.imageTabLayout.addItem(self.imageTabVSpacer)

        self.labelFrameCount = QLabel(self.imageTab)
        self.labelFrameCount.setObjectName(u"labelFrameCount")
        self.labelFrameCount.setAlignment(Qt.AlignCenter)

        self.imageTabLayout.addWidget(self.labelFrameCount)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.priorFrame = QPushButton(self.imageTab)
        self.priorFrame.setObjectName(u"priorFrame")

        self.horizontalLayout.addWidget(self.priorFrame)

        self.frameSelection = QSlider(self.imageTab)
        self.frameSelection.setObjectName(u"frameSelection")
        self.frameSelection.setMinimumSize(QSize(0, 50))
        self.frameSelection.setOrientation(Qt.Horizontal)

        self.horizontalLayout.addWidget(self.frameSelection)

        self.nextFrame = QPushButton(self.imageTab)
        self.nextFrame.setObjectName(u"nextFrame")

        self.horizontalLayout.addWidget(self.nextFrame)

        self.saveImage = QPushButton(self.imageTab)
        self.saveImage.setObjectName(u"saveImage")

        self.horizontalLayout.addWidget(self.saveImage)


        self.imageTabLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.imageTabLayout)

        self.tabWidget.addTab(self.imageTab, "")
        self.calTab = QWidget()
        self.calTab.setObjectName(u"calTab")
        self.calTab.setEnabled(True)
        sizePolicy.setHeightForWidth(self.calTab.sizePolicy().hasHeightForWidth())
        self.calTab.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.calTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.calibrationPlotContainer = QWidget(self.calTab)
        self.calibrationPlotContainer.setObjectName(u"calibrationPlotContainer")
        self.calibrationPlotContainer.setMinimumSize(QSize(0, 500))
        self.calPlotLayout = QVBoxLayout(self.calibrationPlotContainer)
        self.calPlotLayout.setObjectName(u"calPlotLayout")

        self.verticalLayout_2.addWidget(self.calibrationPlotContainer)

        self.calCoefficientLayout = QHBoxLayout()
        self.calCoefficientLayout.setObjectName(u"calCoefficientLayout")
        self.rowLayout = QVBoxLayout()
        self.rowLayout.setObjectName(u"rowLayout")
        self.rowLayout.setContentsMargins(100, -1, 100, -1)
        self.labelRow = QLabel(self.calTab)
        self.labelRow.setObjectName(u"labelRow")
        self.labelRow.setMaximumSize(QSize(200, 30))
        self.labelRow.setAlignment(Qt.AlignCenter)

        self.rowLayout.addWidget(self.labelRow)

        self.rowTextEdit = QPlainTextEdit(self.calTab)
        self.rowTextEdit.setObjectName(u"rowTextEdit")
        self.rowTextEdit.setMaximumSize(QSize(70, 35))
        self.rowTextEdit.setFont(font)

        self.rowLayout.addWidget(self.rowTextEdit)


        self.calCoefficientLayout.addLayout(self.rowLayout)

        self.colLayout = QVBoxLayout()
        self.colLayout.setSpacing(6)
        self.colLayout.setObjectName(u"colLayout")
        self.colLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.colLayout.setContentsMargins(100, -1, 100, -1)
        self.labelCol = QLabel(self.calTab)
        self.labelCol.setObjectName(u"labelCol")
        self.labelCol.setMinimumSize(QSize(50, 0))
        self.labelCol.setMaximumSize(QSize(100, 30))
        self.labelCol.setAlignment(Qt.AlignCenter)

        self.colLayout.addWidget(self.labelCol)

        self.colTextEdit = QPlainTextEdit(self.calTab)
        self.colTextEdit.setObjectName(u"colTextEdit")
        self.colTextEdit.setMinimumSize(QSize(70, 30))
        self.colTextEdit.setMaximumSize(QSize(70, 35))
        self.colTextEdit.setFont(font)

        self.colLayout.addWidget(self.colTextEdit)


        self.calCoefficientLayout.addLayout(self.colLayout)

        self.calCoeffLabelLayout = QVBoxLayout()
        self.calCoeffLabelLayout.setObjectName(u"calCoeffLabelLayout")
        self.calCoeffLabelLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.labelCalCoef = QLabel(self.calTab)
        self.labelCalCoef.setObjectName(u"labelCalCoef")
        self.labelCalCoef.setMinimumSize(QSize(405, 30))
        self.labelCalCoef.setMaximumSize(QSize(500, 16777215))
        self.labelCalCoef.setAlignment(Qt.AlignCenter)

        self.calCoeffLabelLayout.addWidget(self.labelCalCoef)

        self.gainbiasLayout = QHBoxLayout()
        self.gainbiasLayout.setObjectName(u"gainbiasLayout")
        self.labelGain = QLabel(self.calTab)
        self.labelGain.setObjectName(u"labelGain")
        self.labelGain.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gainbiasLayout.addWidget(self.labelGain)

        self.labelGainCoeff = QLabel(self.calTab)
        self.labelGainCoeff.setObjectName(u"labelGainCoeff")

        self.gainbiasLayout.addWidget(self.labelGainCoeff)

        self.labelBias = QLabel(self.calTab)
        self.labelBias.setObjectName(u"labelBias")
        self.labelBias.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gainbiasLayout.addWidget(self.labelBias)

        self.labelBiasCoeff = QLabel(self.calTab)
        self.labelBiasCoeff.setObjectName(u"labelBiasCoeff")

        self.gainbiasLayout.addWidget(self.labelBiasCoeff)


        self.calCoeffLabelLayout.addLayout(self.gainbiasLayout)


        self.calCoefficientLayout.addLayout(self.calCoeffLabelLayout)


        self.verticalLayout_2.addLayout(self.calCoefficientLayout)

        self.calTabSpacer = QSpacerItem(20, 2, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.verticalLayout_2.addItem(self.calTabSpacer)

        self.pushSaveCal = QPushButton(self.calTab)
        self.pushSaveCal.setObjectName(u"pushSaveCal")

        self.verticalLayout_2.addWidget(self.pushSaveCal)

        self.progressbarCal = QProgressBar(self.calTab)
        self.progressbarCal.setObjectName(u"progressbarCal")
        self.progressbarCal.setValue(0)
        self.progressbarCal.setInvertedAppearance(False)

        self.verticalLayout_2.addWidget(self.progressbarCal)

        self.tabWidget.addTab(self.calTab, "")
        self.nedtTab = QWidget()
        self.nedtTab.setObjectName(u"nedtTab")
        self.nedtTab.setEnabled(True)
        sizePolicy.setHeightForWidth(self.nedtTab.sizePolicy().hasHeightForWidth())
        self.nedtTab.setSizePolicy(sizePolicy)
        self.verticalLayout_5 = QVBoxLayout(self.nedtTab)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.widgetNEDTPlot = QWidget(self.nedtTab)
        self.widgetNEDTPlot.setObjectName(u"widgetNEDTPlot")
        self.widgetNEDTPlot.setMinimumSize(QSize(700, 500))
        self.layoutNEDTPlot = QVBoxLayout(self.widgetNEDTPlot)
        self.layoutNEDTPlot.setObjectName(u"layoutNEDTPlot")

        self.verticalLayout_5.addWidget(self.widgetNEDTPlot)

        self.layoutNEDTRowCol = QHBoxLayout()
        self.layoutNEDTRowCol.setObjectName(u"layoutNEDTRowCol")
        self.layoutNEDTRow = QVBoxLayout()
        self.layoutNEDTRow.setObjectName(u"layoutNEDTRow")
        self.layoutNEDTRow.setContentsMargins(200, -1, 200, -1)
        self.labelNEDTRow = QLabel(self.nedtTab)
        self.labelNEDTRow.setObjectName(u"labelNEDTRow")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelNEDTRow.sizePolicy().hasHeightForWidth())
        self.labelNEDTRow.setSizePolicy(sizePolicy2)
        self.labelNEDTRow.setMinimumSize(QSize(0, 0))
        self.labelNEDTRow.setMaximumSize(QSize(200, 30))
        self.labelNEDTRow.setAlignment(Qt.AlignCenter)

        self.layoutNEDTRow.addWidget(self.labelNEDTRow)

        self.texteditNEDTRow = QTextEdit(self.nedtTab)
        self.texteditNEDTRow.setObjectName(u"texteditNEDTRow")
        sizePolicy.setHeightForWidth(self.texteditNEDTRow.sizePolicy().hasHeightForWidth())
        self.texteditNEDTRow.setSizePolicy(sizePolicy)
        self.texteditNEDTRow.setMinimumSize(QSize(70, 35))
        self.texteditNEDTRow.setMaximumSize(QSize(70, 35))
        self.texteditNEDTRow.setFont(font)

        self.layoutNEDTRow.addWidget(self.texteditNEDTRow)


        self.layoutNEDTRowCol.addLayout(self.layoutNEDTRow)

        self.layoutNEDTCol = QVBoxLayout()
        self.layoutNEDTCol.setObjectName(u"layoutNEDTCol")
        self.layoutNEDTCol.setContentsMargins(200, -1, 200, -1)
        self.labelNEDTCol = QLabel(self.nedtTab)
        self.labelNEDTCol.setObjectName(u"labelNEDTCol")
        self.labelNEDTCol.setMaximumSize(QSize(200, 30))
        self.labelNEDTCol.setAlignment(Qt.AlignCenter)

        self.layoutNEDTCol.addWidget(self.labelNEDTCol)

        self.texteditNEDTCol = QTextEdit(self.nedtTab)
        self.texteditNEDTCol.setObjectName(u"texteditNEDTCol")
        sizePolicy.setHeightForWidth(self.texteditNEDTCol.sizePolicy().hasHeightForWidth())
        self.texteditNEDTCol.setSizePolicy(sizePolicy)
        self.texteditNEDTCol.setMinimumSize(QSize(70, 35))
        self.texteditNEDTCol.setMaximumSize(QSize(70, 35))
        self.texteditNEDTCol.setFont(font)

        self.layoutNEDTCol.addWidget(self.texteditNEDTCol)


        self.layoutNEDTRowCol.addLayout(self.layoutNEDTCol)


        self.verticalLayout_5.addLayout(self.layoutNEDTRowCol)

        self.pushSaveNEDT = QPushButton(self.nedtTab)
        self.pushSaveNEDT.setObjectName(u"pushSaveNEDT")

        self.verticalLayout_5.addWidget(self.pushSaveNEDT)

        self.tabWidget.addTab(self.nedtTab, "")
        self.stabilityTab = QWidget()
        self.stabilityTab.setObjectName(u"stabilityTab")
        self.stabilityTab.setEnabled(True)
        sizePolicy.setHeightForWidth(self.stabilityTab.sizePolicy().hasHeightForWidth())
        self.stabilityTab.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.stabilityTab)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.stabilityPlotContainer = QWidget(self.stabilityTab)
        self.stabilityPlotContainer.setObjectName(u"stabilityPlotContainer")
        self.stabilityPlotLayout = QVBoxLayout(self.stabilityPlotContainer)
        self.stabilityPlotLayout.setObjectName(u"stabilityPlotLayout")

        self.verticalLayout_6.addWidget(self.stabilityPlotContainer)

        self.progressbarStability = QProgressBar(self.stabilityTab)
        self.progressbarStability.setObjectName(u"progressbarStability")
        self.progressbarStability.setValue(0)

        self.verticalLayout_6.addWidget(self.progressbarStability)

        self.tabWidget.addTab(self.stabilityTab, "")

        self.mainHorzLayout.addWidget(self.tabWidget)


        self.verticalLayout.addLayout(self.mainHorzLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1438, 23))
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
        self.actionOpen_Project.setText(QCoreApplication.translate("MainWindow", u"Open Project", None))
        self.actionSave_Project.setText(QCoreApplication.translate("MainWindow", u"Save Project", None))
        self.actionNew_Project.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
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

        self.imagelabel.setText("")
        self.labelFrameCount.setText(QCoreApplication.translate("MainWindow", u"Current Frame: 0 of 0.", None))
        self.priorFrame.setText(QCoreApplication.translate("MainWindow", u"<", None))
        self.nextFrame.setText(QCoreApplication.translate("MainWindow", u">", None))
        self.saveImage.setText(QCoreApplication.translate("MainWindow", u"Save Image", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.imageTab), QCoreApplication.translate("MainWindow", u"Image Preview", None))
        self.labelRow.setText(QCoreApplication.translate("MainWindow", u"Row", None))
        self.rowTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"1", None))
        self.labelCol.setText(QCoreApplication.translate("MainWindow", u"Column", None))
        self.colTextEdit.setPlainText(QCoreApplication.translate("MainWindow", u"1", None))
        self.labelCalCoef.setText(QCoreApplication.translate("MainWindow", u"Calibration Coefficients", None))
        self.labelGain.setText(QCoreApplication.translate("MainWindow", u"Gain :", None))
        self.labelGainCoeff.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.labelBias.setText(QCoreApplication.translate("MainWindow", u"Bias : ", None))
        self.labelBiasCoeff.setText(QCoreApplication.translate("MainWindow", u"0.00", None))
        self.pushSaveCal.setText(QCoreApplication.translate("MainWindow", u"Save Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.calTab), QCoreApplication.translate("MainWindow", u"Calibrate", None))
        self.labelNEDTRow.setText(QCoreApplication.translate("MainWindow", u"Row", None))
        self.texteditNEDTRow.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">1</span></p></body></html>", None))
        self.labelNEDTCol.setText(QCoreApplication.translate("MainWindow", u"Column", None))
        self.texteditNEDTCol.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:'Noto Sans'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'Sans Serif';\">1</span></p></body></html>", None))
        self.pushSaveNEDT.setText(QCoreApplication.translate("MainWindow", u"Save NEDT Plot", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.nedtTab), QCoreApplication.translate("MainWindow", u"NEDT", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.stabilityTab), QCoreApplication.translate("MainWindow", u"Stability", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuWorkflow.setTitle(QCoreApplication.translate("MainWindow", u"Workflow", None))
    # retranslateUi

