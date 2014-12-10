#!/usr/bin/env python
# -*- coding: utf8 -*-
import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.createToolBox()
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createStatusBar()
        self.createDockWindows()
        self.setWindowTitle("Dock Widgets")
        self.setUnifiedTitleAndToolBarOnMac(True)

    def about(self):
        QtGui.QMessageBox.about(self, "About Dock Widgets",
                "The <b>Dock Widgets</b> example demonstrates how to use "
                "Qt's dock widgets. You can enter your own text, click a "
                "customer to add a customer name and address, and click "
                "standard paragraphs to add them.")

    def createActions(self):
        #self.saveAct = QtGui.QAction(QtGui.QIcon(':/images/save.png'),
                #"&Save...", self, shortcut=QtGui.QKeySequence.Save,
                #statusTip="Save the current form letter",
                #triggered=self.save)


        self.quitAct = QtGui.QAction("&Quit", self, shortcut="Ctrl+Q",
                statusTip="Quit the application", triggered=self.close)

        self.aboutAct = QtGui.QAction("&About", self,
                statusTip="Show the application's About box",
                triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                statusTip="Show the Qt library's About box",
                triggered=QtGui.qApp.aboutQt)

    def createMenus(self):
        self.fileMenu = self.menuBar().addMenu("&File")
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.quitAct)
        self.viewMenu = self.menuBar().addMenu("&View")

        self.menuBar().addSeparator()

        self.helpMenu = self.menuBar().addMenu("&Help")
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

    def createToolBars(self):
        self.fileToolBar = self.addToolBar("File")
        self.fileToolBar.addAction(self.aboutQtAct)

        self.editToolBar = self.addToolBar("Edit")
        self.fileToolBar.addAction(self.quitAct)

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")

    def createDockWindows(self):
        # Ipython命令栏
        dock = QtGui.QDockWidget("Paragraphs", self)
        self.paragraphsList = QtGui.QListWidget(dock)
        self.paragraphsList.addItems((
            "Thank you for your payment which we have received today.",
            "Your order has been dispatched and should be with you within "
                "28 days.",
            "You made an overpayment (more than $5). Do you wish to buy more "
                "items, or should we return the excess to you?"))
        dock.setWidget(self.paragraphsList)
        dock.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.TopDockWidgetArea)
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())
        # ToolBox工具栏
        dock = QtGui.QDockWidget("Customers", self)
        dock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        dock.setWidget(self.toolBox)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)
        self.viewMenu.addAction(dock.toggleViewAction())

        #self.customerList.currentTextChanged.connect(self.insertCustomer)
        #self.paragraphsList.currentTextChanged.connect(self.addParagraph)

    def createToolBox(self):
        self.buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup.setExclusive(False)
        #self.buttonGroup.buttonClicked[int].connect(self.buttonGroupClicked)

        layout = QtGui.QGridLayout()
        #layout.addWidget(self.createCellWidget("Conditional", DiagramItem.Conditional), 0, 0)
        #layout.addWidget(self.createCellWidget("Process", DiagramItem.Step), 0, 1)
        #layout.addWidget(self.createCellWidget("Input/Output", DiagramItem.Io), 1, 0)

        textButton = QtGui.QToolButton()
        textButton.setCheckable(True)
        textButton.setIcon(QtGui.QIcon(QtGui.QPixmap(':/images/textpointer.png')
                            .scaled(30, 30)))
        textButton.setIconSize(QtCore.QSize(50, 50))

        textLayout = QtGui.QGridLayout()
        textLayout.addWidget(textButton, 0, 0, QtCore.Qt.AlignHCenter)
        textLayout.addWidget(QtGui.QLabel("Text"), 1, 0,
                QtCore.Qt.AlignCenter)
        textWidget = QtGui.QWidget()
        textWidget.setLayout(textLayout)
        layout.addWidget(textWidget, 1, 1)

        layout.setRowStretch(3, 10)
        layout.setColumnStretch(2, 10)

        itemWidget = QtGui.QWidget()
        itemWidget.setLayout(layout)

        self.backgroundButtonGroup = QtGui.QButtonGroup()
        #self.backgroundButtonGroup.buttonClicked.connect(self.backgroundButtonGroupClicked)

        backgroundLayout = QtGui.QGridLayout()
        backgroundLayout.addWidget(self.createBackgroundCellWidget("Blue Grid",
                ':/images/background1.png'), 0, 0)
        backgroundLayout.addWidget(self.createBackgroundCellWidget("White Grid",
                ':/images/background2.png'), 0, 1)
        backgroundLayout.addWidget(self.createBackgroundCellWidget("Gray Grid",
                ':/images/background3.png'), 1, 0)
        backgroundLayout.addWidget(self.createBackgroundCellWidget("No Grid",
                ':/images/background4.png'), 1, 1)

        backgroundLayout.setRowStretch(2, 10)
        backgroundLayout.setColumnStretch(2, 10)

        backgroundWidget = QtGui.QWidget()
        backgroundWidget.setLayout(backgroundLayout)

        self.toolBox = QtGui.QToolBox()
        self.toolBox.setSizePolicy(QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Ignored))
        self.toolBox.setMinimumWidth(itemWidget.sizeHint().width())
        self.toolBox.addItem(itemWidget, "Basic Flowchart Shapes")
        self.toolBox.addItem(backgroundWidget, "Backgrounds")

    def createBackgroundCellWidget(self, text, image):
        button = QtGui.QToolButton()
        button.setText(text)
        button.setIcon(QtGui.QIcon(image))
        button.setIconSize(QtCore.QSize(50, 50))
        button.setCheckable(True)
        self.backgroundButtonGroup.addButton(button)

        layout = QtGui.QGridLayout()
        layout.addWidget(button, 0, 0, QtCore.Qt.AlignHCenter)
        layout.addWidget(QtGui.QLabel(text), 1, 0, QtCore.Qt.AlignCenter)

        widget = QtGui.QWidget()
        widget.setLayout(layout)

        return widget


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
