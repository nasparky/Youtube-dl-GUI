import os
import sys
import subprocess
from datetime import datetime
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QThread
from PyQt6.QtWebEngineWidgets import QWebEngineView

from extras import changeName, createDir, calcMissingProp, getHTMLLink, getEmbededLink
from worker import QWorker
from stylesheet import stylesheet

os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1" # Keep control of screen size on re-position of another screen.

defaultWindowSize = (1000, 800)
defaultFontSize = 10
defaultFontSizeSmall = 9

htmlReference = f'''
  <!DOCTYPE html><html style="background-color: #000000;">
  <body></body></html>
'''

class YDLWindow(QtWidgets.QMainWindow):
  def __init__(self):
    super().__init__()
    self.tableModel = QtGui.QStandardItemModel()
    self.tableModel.setHorizontalHeaderLabels(["Id", "Link", "Type", "Playlist?"])

  def setup(self):
    # Setup Window
    self.setObjectName("MainWindow")
    self.setMinimumWidth(defaultWindowSize[0])
    self.setMinimumHeight(defaultWindowSize[1])
    self.resize(defaultWindowSize[0], defaultWindowSize[1])
    self.setWindowIcon(QtGui.QIcon('favicon.ico'))

    # Setup Central Widget
    self.centralWidget = QtWidgets.QWidget(self)
    self.centralWidget.setObjectName("CentralWidget")
    self.gridLayoutCentralWidget = QtWidgets.QGridLayout(self.centralWidget)
    self.gridLayoutCentralWidget.setObjectName("GridLayoutCentralWidget")
    self.setCentralWidget(self.centralWidget)

    # Setup Tabs
    self.tabWidget = QtWidgets.QTabWidget(self.centralWidget)
    self.tabWidget.setObjectName("TabWidget")
    self.tabCore = QtWidgets.QWidget()
    self.tabCore.setObjectName("TabCore")
    self.tabWidget.addTab(self.tabCore, "")
    self.gridLayoutCentralWidget.addWidget(self.tabWidget, 0, 0, 1, 1)
    self.gridLayoutCore = QtWidgets.QGridLayout(self.tabCore)
    self.gridLayoutCore.setObjectName("GridLayoutCore")
    self.gridLayoutCore.setColumnStretch(0, 1)  # Fix layout issue with spacing
    self.gridLayoutCore.setColumnStretch(1, 1)
    self.gridLayoutCore.setRowStretch(0, 1)
    self.gridLayoutCore.setRowStretch(1, 1)
    self.gridLayoutCore.setRowStretch(2, 1)

    # Setup Tab information (Core)
    # Terminal
    self.groupBoxTerminal = QtWidgets.QGroupBox(self.tabCore)
    self.groupBoxTerminal.setObjectName("GroupBoxTerminal")
    self.gridLayoutCore.addWidget(self.groupBoxTerminal, 0, 0, 1, 1)
    self.gridLayoutTerminal = QtWidgets.QGridLayout(self.groupBoxTerminal)
    self.gridLayoutTerminal.setObjectName("GridLayoutTerminal")

    self.textEditTerminal = QtWidgets.QTextEdit(self.groupBoxTerminal)
    self.textEditTerminal.setAcceptDrops(False)
    self.textEditTerminal.setReadOnly(True)
    self.textEditTerminal.setPlaceholderText("")
    self.textEditTerminal.setObjectName("TextEditTerminal")
    self.gridLayoutTerminal.addWidget(self.textEditTerminal, 0, 0, 1, 1)

    # Queue
    self.groupBoxQueue = QtWidgets.QGroupBox(self.tabCore)
    self.groupBoxQueue.setObjectName("GroupBoxQueue")
    self.gridLayoutCore.addWidget(self.groupBoxQueue, 0, 1, 3, 1)
    self.gridLayoutQueue = QtWidgets.QGridLayout(self.groupBoxQueue)
    self.gridLayoutQueue.setObjectName("GridLayoutQueue")
    self.gridLayoutQueue.setRowStretch(0, 1)
    self.gridLayoutQueue.setRowStretch(1, 1)
    self.gridLayoutQueue.setRowStretch(2, 1)
    self.gridLayoutQueue.setColumnStretch(0, 1)
    self.gridLayoutQueue.setColumnStretch(1, 1)
    self.gridLayoutQueue.setColumnStretch(2, 1)

    self.tableViewQueue = QtWidgets.QTableView()
    self.tableViewQueue.setModel(self.tableModel)
    self.tableViewQueue.setWordWrap(True)
    self.gridLayoutQueue.addWidget(self.tableViewQueue, 0, 0, 1, 3)

    self.comboBoxQueueType = QtWidgets.QComboBox(self.groupBoxQueue)
    self.comboBoxQueueType.setObjectName("ComboBoxQueueType")
    self.comboBoxQueueType.addItem("Video")
    self.comboBoxQueueType.addItem("Audio")
    self.gridLayoutQueue.addWidget(self.comboBoxQueueType, 1, 0, 1, 1)

    self.pushButtonQueueRemove = QtWidgets.QPushButton(self.groupBoxQueue)
    self.pushButtonQueueRemove.setObjectName("PushButtonQueueRemove")
    self.gridLayoutQueue.addWidget(self.pushButtonQueueRemove, 1, 1, 1, 1)

    self.pushButtonQueueClear = QtWidgets.QPushButton(self.groupBoxQueue)
    self.pushButtonQueueClear.setObjectName("PushButtonQueueClear")
    self.gridLayoutQueue.addWidget(self.pushButtonQueueClear, 1, 2, 1, 1)

    self.checkBoxPlaylist = QtWidgets.QCheckBox(self.groupBoxQueue)
    self.checkBoxPlaylist.setObjectName("CheckBoxPlaylist")
    self.gridLayoutQueue.addWidget(self.checkBoxPlaylist, 2, 0, 1, 1)

    self.pushButtonQueueOpen = QtWidgets.QPushButton(self.groupBoxQueue)
    self.pushButtonQueueOpen.setObjectName("PushButtonQueueOpen")
    self.gridLayoutQueue.addWidget(self.pushButtonQueueOpen, 2, 1, 1, 2)

    self.labelQueueLink = QtWidgets.QLabel(self.groupBoxQueue)
    self.labelQueueLink.setObjectName("LabelQueueLink")
    self.labelQueueLink.setFont(QtGui.QFont("Monospace", defaultFontSize))
    self.gridLayoutQueue.addWidget(self.labelQueueLink, 3, 0, 1, 1)

    self.lineEditQueueLink = QtWidgets.QLineEdit(self.groupBoxQueue)
    self.lineEditQueueLink.setObjectName("LineEditQueueLink")
    self.gridLayoutQueue.addWidget(self.lineEditQueueLink, 3, 1, 1, 2)

    # Preview
    self.groupBoxPreview = QtWidgets.QGroupBox(self.tabCore)
    self.groupBoxPreview.setObjectName("GroupBoxPreview")
    self.gridLayoutCore.addWidget(self.groupBoxPreview, 1, 0, 2, 1)
    self.gridLayoutPreview = QtWidgets.QGridLayout(self.groupBoxPreview)
    self.gridLayoutPreview.setObjectName("GridLayoutPreview")

    self.webEngineViewPreview = QWebEngineView(self.groupBoxPreview)
    self.webEngineViewPreview.setObjectName("WebEngineViewPreview")
    self.webEngineViewPreview.setHtml(htmlReference)
    self.gridLayoutPreview.addWidget(self.webEngineViewPreview, 0, 0, 1, 1)

    # Progress
    self.groupBoxProgress = QtWidgets.QGroupBox(self.tabCore)
    self.groupBoxProgress.setObjectName("GroupBoxProgress")
    self.gridLayoutCore.addWidget(self.groupBoxProgress, 3, 0, 1, 2)
    self.gridLayoutProgress = QtWidgets.QGridLayout(self.groupBoxProgress)
    self.gridLayoutProgress.setObjectName("GridLayoutProgress")

    self.pushButtonProgressDownload = QtWidgets.QPushButton(self.groupBoxQueue)
    self.pushButtonProgressDownload.setObjectName("PushButtonProgressDownload")
    self.gridLayoutProgress.addWidget(self.pushButtonProgressDownload, 0, 0, 1, 1)

    self.pushButtonProgressPush = QtWidgets.QPushButton(self.groupBoxQueue)
    self.pushButtonProgressPush.setObjectName("PushButtonProgressPush")
    self.gridLayoutProgress.addWidget(self.pushButtonProgressPush, 0, 1, 1, 1)

    self.progressBarProgress = QtWidgets.QProgressBar(self.groupBoxProgress)
    self.progressBarProgress.setObjectName("ProgressBarProgress")
    self.progressBarProgress.setProperty("value", 0)
    self.progressBarProgress.setTextVisible(True)
    self.progressBarProgress.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
    self.progressBarProgress.setMinimum(0)
    self.progressBarProgress.setMaximum(100)
    self.gridLayoutProgress.addWidget(self.progressBarProgress, 1, 0, 1, 2)

    # Setup Menubar
    self.menuBar = QtWidgets.QMenuBar(self)
    self.menuBar.setObjectName("MenuBar")
    self.setMenuBar(self.menuBar)
    self.menuFile = QtWidgets.QMenu(self.menuBar)
    self.menuFile.setObjectName("MenuFile")
    self.actionOpen = QtGui.QAction(self)
    self.actionOpen.setObjectName("ActionOpen")
    self.actionSave = QtGui.QAction(self)
    self.actionSave.setObjectName("ActionSave")
    self.actionExit = QtGui.QAction(self)
    self.actionExit.setObjectName("ActionExit")
    self.menuFile.addAction(self.actionOpen)
    self.menuFile.addAction(self.actionSave)
    self.menuFile.addAction(self.actionExit)
    self.menuBar.addAction(self.menuFile.menuAction())

    # Setup other information
    self.translateUI()
    self.__triggerEvents()
    self.__reportTerminalMessage("Completed Setup")

  def translateUI(self):
    translate = QtCore.QCoreApplication.translate
    self.setWindowTitle(translate("MainWindow", "Youtube Video Downloader"))
    self.menuFile.setTitle(translate("MainWindow", "File"))
    self.actionOpen.setText(translate("MainWindow", "Open"))
    self.actionSave.setText(translate("MainWindow", "Save"))
    self.actionExit.setText(translate("MainWindow", "Exit"))
    self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabCore), translate("MainWindow", "Download"))
    self.groupBoxTerminal.setTitle(translate("MainWindow", "Terminal"))
    self.groupBoxQueue.setTitle(translate("MainWindow", "Queue"))
    self.groupBoxPreview.setTitle(translate("MainWindow", "Preview"))
    self.groupBoxProgress.setTitle(translate("MainWindow", "Progress"))
    self.comboBoxQueueType.setItemText(0, translate("MainWindow", "Video"))
    self.comboBoxQueueType.setItemText(1, translate("MainWindow", "Audio"))
    self.pushButtonQueueRemove.setText(translate("MainWindow", "Remove"))
    self.pushButtonQueueClear.setText(translate("MainWindow", "Clear"))
    self.labelQueueLink.setText(translate("MainWindow", "Link"))
    self.checkBoxPlaylist.setText(translate("MainWindow", "Playlist?"))
    self.pushButtonQueueOpen.setText(translate("MainWindow", "Open File Location"))
    self.pushButtonProgressDownload.setText(translate("MainWindow", "Download"))
    self.pushButtonProgressPush.setText(translate("MainWindow", "Push to queue"))  

  def resizeEvent(self, event):
    fontSize = calcMissingProp(defaultWindowSize[1], self.frameGeometry().height(), defaultFontSize)
    fontSizeSmall = calcMissingProp(defaultWindowSize[1], self.frameGeometry().height(), defaultFontSizeSmall)
    self.tabCore.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.groupBoxTerminal.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.groupBoxQueue.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.groupBoxPreview.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.groupBoxProgress.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.comboBoxQueueType.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.comboBoxQueueType.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.pushButtonQueueRemove.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.pushButtonQueueClear.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.labelQueueLink.setFont(QtGui.QFont("Monospace", fontSize))
    self.checkBoxPlaylist.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.textEditTerminal.setFont(QtGui.QFont("Consolas", fontSizeSmall))
    self.lineEditQueueLink.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.tableViewQueue.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.pushButtonQueueOpen.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.pushButtonProgressDownload.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.pushButtonProgressPush.setFont(QtGui.QFont("Monospace", fontSizeSmall))
    self.progressBarProgress.setFont(QtGui.QFont("Monospace", fontSizeSmall))

  def __reportTerminalMessage(self, text):
    newText = "{}{} - {}".format(self.textEditTerminal.toPlainText(), datetime.now().strftime("%H:%M:%S"), text+"\n")
    self.textEditTerminal.setText(newText)
    self.textEditTerminal.verticalScrollBar().setValue(self.textEditTerminal.verticalScrollBar().maximum())

  def __triggerEvents(self):
    self.pushButtonProgressPush.clicked.connect(lambda: self.__pushButtonPushEvent())
    self.pushButtonProgressDownload.clicked.connect(lambda: self.__pushButtonDownloadEvent())
    self.pushButtonQueueRemove.clicked.connect(lambda: self.__pushButtonRemoveEvent())
    self.pushButtonQueueClear.clicked.connect(lambda: self.__pushButtonClearEvent())
    self.pushButtonQueueOpen.clicked.connect(lambda: self.__pushButtonOpenEvent())

  def __pushButtonPushEvent(self):
    linkAddress = self.lineEditQueueLink.text() # Get link text from the line edit widget
    if linkAddress != "" and linkAddress != None:
      embededLink = getEmbededLink(linkAddress) # Get embeded text for web engine widget
      if embededLink != None:
        self.webEngineViewPreview.setHtml(  # Create new html video preview
          getHTMLLink([self.webEngineViewPreview.frameGeometry().width(), 
                       self.webEngineViewPreview.frameGeometry().height()],
                      embededLink))
        self.__reportTerminalMessage("Successfully created new preview.")
        self.tableModel.appendRow(  # Set a new row with data
          [QtGui.QStandardItem(str(self.tableModel.rowCount() + 1)), 
           QtGui.QStandardItem(linkAddress), 
           QtGui.QStandardItem(self.comboBoxQueueType.currentText()),
           QtGui.QStandardItem(str(self.checkBoxPlaylist.isChecked()))])
        self.tableViewQueue.setModel(self.tableModel) # Restate new data
        self.lineEditQueueLink.setText("") # Reset text link box
        self.__reportTerminalMessage("Successfully added new link.")
      else:
        self.__reportTerminalMessage("Invalid link, aborting load.")
    else:
      self.__reportTerminalMessage("Unable to acquire anything from an empty link address.")

  def __pushButtonDownloadEvent(self):
    try:
      self.__reportTerminalMessage(createDir())
      self.__disableWidgets()
      queue = []
      for r in range(self.tableModel.rowCount()):
        queue.append([self.tableModel.item(r, c).text()
          for c in range(self.tableModel.columnCount())])
      if len(queue) != 0:
        self.thread = QThread()
        self.worker = QWorker(queue)
        self.worker.moveToThread(self.thread)
        #self.thread.started.connect(lambda: self.worker.run(queue))
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.__progressBarEvent)
        self.worker.logger.connect(self.__reportTerminalMessage)
        self.__reportTerminalMessage("Successful thread creation.")
        self.__reportTerminalMessage("Starting thread work...")
        self.thread.start()
        self.__pushButtonClearEvent()
        self.thread.finished.connect(self.__enableWidgets)
      else:
        self.__reportTerminalMessage("There is nothing to download.")
        self.__enableWidgets()
    except Exception as e:
      self.__reportTerminalMessage("Unable to continue, client or server side issue.")
      print(e)
      print("From YDLMainWindow")
      self.__enableWidgets()

  def __pushButtonRemoveEvent(self):
    if self.tableModel.rowCount() > 0:
      self.tableModel.removeRow(self.tableModel.rowCount() - 1)
      self.tableViewQueue.setModel(self.tableModel)
      self.__reportTerminalMessage("Successfully removed the last row.")
    else:
      self.__reportTerminalMessage("Insufficient number of rows to remove.")

  def __pushButtonClearEvent(self):
    if self.tableModel.rowCount() > 0:
      self.tableModel.clear()
      self.tableModel.setHorizontalHeaderLabels(["Id", "Link", "Type", "Playlist?"])
      self.tableViewQueue.setModel(self.tableModel)
      self.__reportTerminalMessage("Successfully cleared the table.")
    else:
      self.__reportTerminalMessage("Table is already cleared.")

  def __pushButtonOpenEvent(self):
    try:
      self.__reportTerminalMessage("Opening up export directory.")
      subprocess.Popen(f"explorer {os.path.join(os.getcwd(), 'Exports')}")
    except OSError as e:
      self.__reportTerminalMessage("Could not open export directory.")

  def __progressBarEvent(self, fProg, iProg):
    if fProg == (-1*1.0) and iProg == 0:
      self.progressBarProgress.reset()
    else:
      self.progressBarProgress.setValue(fProg)
      #self.labelQueueLink.setText("ETA: " + str(iProg) + " s")

  def __disableWidgets(self):
    self.comboBoxQueueType.setEnabled(False)
    self.checkBoxPlaylist.setEnabled(False)
    self.lineEditQueueLink.setEnabled(False)
    self.pushButtonProgressPush.setEnabled(False)
    self.pushButtonProgressDownload.setEnabled(False)
    self.pushButtonQueueRemove.setEnabled(False)
    self.pushButtonQueueClear.setEnabled(False)
    self.__reportTerminalMessage("Successfully disabled all user options.")

  def __enableWidgets(self):
    self.comboBoxQueueType.setEnabled(True)
    self.checkBoxPlaylist.setEnabled(True)
    self.lineEditQueueLink.setEnabled(True)
    self.pushButtonProgressPush.setEnabled(True)
    self.pushButtonProgressDownload.setEnabled(True)
    self.pushButtonQueueRemove.setEnabled(True)
    self.pushButtonQueueClear.setEnabled(True)
    self.__reportTerminalMessage("Successfully re-enabled all user options.")

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  app.setStyleSheet(stylesheet)
  mainWindow = YDLWindow()
  mainWindow.setup()
  mainWindow.show()
  sys.exit(app.exec())

"""
https://youtu.be/uQ-35vZHvqk
"""