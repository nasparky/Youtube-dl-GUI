# -*- coding: utf-8 -*-
#
# Form implementation generated from reading ui file 'Project Files/YoutubeDL.ui'
#
# Created by: PyQt5 UI code generator 5.15.4

import os
import youtube_dl as yt
from threading import Thread
from collections import deque
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QObject, QThread, pyqtSignal
from PyQt5.QtWebEngineWidgets import QWebEngineView
    

def changeName(filename):
    new_filename = ""
    schars = ['?','/','\\','|','"',';',',','”',':','.',"'","~"]
    for c in filename:
        for sc in schars:   # Very Expensive
            if(c == sc):
                c = ""
        new_filename += c
    return new_filename

def createDir():
    try:
        if(not(os.path.isdir(os.getcwd()+"/Exports"))):
            os.mkdir(os.getcwd()+"/Exports")
        return "Successful directory load."
    except OSError as Error:
        return "Error: unable to create a new directory for converted files."

def download(link, progress_hook):
    address = link[0]
    type = link[1].replace("\n", "")
    '''
    ydl_opts = {
        'outtmpl': path + name
        'format': 'bestvideo[ext=mp4]/best+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'quiet' : False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }
    '''
    ydl_opts = {}
    if(type == "MP3"):
        ydl_opts = {
            'outtmpl': 'Exports/%(title)s - %(id)s.%(ext)s',
            'format': 'bestaudio/bestaudio[ext=m4a]/best',
            'quiet' : True,
            'progress_hooks': [progress_hook],
        }
    elif(type == "MP4"):
        ydl_opts = {
            'outtmpl': 'Exports/%(title)s - %(id)s.%(ext)s',
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'quiet' : True,
            'progress_hooks': [progress_hook],
        }
    with yt.YoutubeDL(ydl_opts) as y:
        y.download([address])
    
class Ui_MainWindow(object):
    # Does not effect the setup process
    def __init__(self):
        self.queue = deque()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        MainWindow.setMouseTracking(False)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMouseTracking(False)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(30, 486, 351, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(410, 486, 361, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(30, 550, 691, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 525, 61, 21))
        self.label.setObjectName("label")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(410, 40, 361, 311))
        self.textEdit.setAcceptDrops(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setPlaceholderText("")
        self.textEdit.setObjectName("textEdit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(410, 15, 361, 21))
        self.label_2.setObjectName("label_2")
        self.textEdit_2 = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit_2.setGeometry(QtCore.QRect(30, 40, 351, 81))
        self.textEdit_2.setAcceptDrops(False)
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setAcceptRichText(False)
        self.textEdit_2.setObjectName("textEdit_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 15, 351, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 135, 351, 21))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(410, 440, 361, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(410, 420, 35, 16))
        self.label_5.setObjectName("label_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 360, 81, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(680, 360, 91, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(410, 370, 62, 21))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton_2.setGeometry(QtCore.QRect(470, 370, 62, 21))
        self.radioButton_2.setObjectName("radioButton_2")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(720, 550, 61, 21))
        self.label_6.setObjectName("label_6")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 170, 351, 291))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        MainWindow.setCentralWidget(self.centralwidget)

        # Web file renderer
        self.preview = QWebEngineView(self.centralwidget)
        self.preview.setGeometry(QtCore.QRect(30, 170, 351, 291))
        self.preview.setObjectName("player")
        
        self.retranslateUi(MainWindow)
        self.triggerEventsUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YoutubeDL"))
        self.pushButton.setText(_translate("MainWindow", "Download"))
        self.pushButton_2.setText(_translate("MainWindow", "Push to Queue"))
        self.label.setText(_translate("MainWindow", "Progress Bar"))
        self.label_2.setText(_translate("MainWindow", "Queue List"))
        self.label_3.setText(_translate("MainWindow", "Terminal Actions"))
        self.label_4.setText(_translate("MainWindow", "Preview"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter a link address here."))
        self.label_5.setText(_translate("MainWindow", "Link"))
        self.pushButton_3.setText(_translate("MainWindow", "Remove"))
        self.pushButton_4.setText(_translate("MainWindow", "Clear"))
        self.radioButton.setText(_translate("MainWindow", "MP3"))
        self.radioButton_2.setText(_translate("MainWindow", "MP4"))
        self.label_6.setText(_translate("MainWindow", "ETA: 0s"))

    def triggerEventsUi(self):
        #self.pushButton.clicked.connect(lambda _:self.textEdit.setText("Clicked"))
        self.pushButton.clicked.connect(lambda _:Thread(target=self.__eventP1, daemon=True).run())
        self.pushButton_2.clicked.connect(lambda _:self.__eventP2())
        self.pushButton_3.clicked.connect(lambda _:self.__eventP3())
        self.pushButton_4.clicked.connect(lambda _:self.__eventP4())
    
    def __recordTerminalEvent(self, text):
        new_text = "{}{} - {}".format(self.textEdit_2.toPlainText(), datetime.now().strftime("%H:%M:%S"), text+"\n")
        self.textEdit_2.setText(new_text)
        self.textEdit_2.verticalScrollBar().setValue(self.textEdit_2.verticalScrollBar().maximum())

    def __eventP1(self):
        try:
            new_queue = self.textEdit.toPlainText()
            new_address = ""
            self.__recordTerminalEvent("Attempting to place text into queue.")
            for c in new_queue:
                if(c == "\n"):
                    self.queue.append(new_address)
                    new_address = ""
                else:
                    new_address += c
            print(self.queue)
            self.__recordTerminalEvent(createDir())
            self.__recordTerminalEvent("Starting link download operation.")
            initial_length = len(self.queue)
            while(len(self.queue) != 0):
                link = self.queue.pop().split("|")
                self.__recordTerminalEvent("Batch: {}/{} - {}".format((-1*(len(self.queue)))+initial_length, initial_length, link))
                #Thread(target=download, args=(link, self.__eventPB1), daemon=True).run()
                download(link, self.__eventPB1)
            self.textEdit.setText("")
            self.__recordTerminalEvent("Operation(s) Successful.")
        except:
            self.__recordTerminalEvent("FAILED to download addresses from the queue.")
    
    def __eventP2(self):
        address = self.lineEdit.text()
        unique_str = "-1"
        self.__recordTerminalEvent("Retrieving unique specifier.")
        if(address.find("https://youtu.be/") != -1):
            unique_str = address.replace("https://youtu.be/", "")
        elif(address.find("https://www.youtube.com/watch?v=") != -1):
            unique_str = address.replace("https://www.youtube.com/watch?v=", "")
        else:
            self.__recordTerminalEvent("Invalid link, cannot display.")
        self.__recordTerminalEvent("Creating a new preview.")
        self.preview.setHtml('''
            <!DOCTYPE html>
                <html>
                    <body>
                        <iframe width="340" height="280" src={} title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                    </body>
                </html>'''.format("http://www.youtube.com/embed/"+unique_str))

        self.lineEdit.setText("")
        self.__recordTerminalEvent("Checking for format choice.")
        if(self.radioButton.isChecked()):
            self.textEdit.setText("{}{}|{}".format(self.textEdit.toPlainText(), address, "MP3\n"))
            self.__recordTerminalEvent("Pushing the new address.")
        elif(self.radioButton_2.isChecked()):
            self.textEdit.setText("{}{}|{}".format(self.textEdit.toPlainText(), address, "MP4\n"))
            self.__recordTerminalEvent("Pushing the new address.")
        else:
            self.__recordTerminalEvent("Failed to identify type.")
    
    def __eventP3(self):
        if(self.textEdit.toPlainText() == ""):
            self.__recordTerminalEvent("Cannot remove a queue list that is empty.")
        else:
            substring = self.textEdit.toPlainText().split("\n")
            for index in range(len(substring)):
                if(index == len(substring)-1):
                    self.__recordTerminalEvent("Removing {} from the queue.".format(substring[index-1]))
                    self.textEdit.setText(self.textEdit.toPlainText().replace("{}".format(substring[index-1]+"\n"), ""))

    def __eventP4(self):
        self.__recordTerminalEvent("Clearing current queue list.")
        self.textEdit.setText("")

    def __eventPB1(self, d):
        if d['status'] == 'finished':
            self.progressBar.reset()
            self.__recordTerminalEvent("Download Complete.")
        if d['status'] == 'downloading':
            p = d['_percent_str']
            p = p.replace('%','')
            #print(d['eta'])
            self.progressBar.setValue(float(p))
            self.label_6.setText("ETA: "+str(d['eta'])+"s")

    def _thread_task(self):
        new_thread = QThread()
        new_thread.start()

'<iframe width="1314" height="748" src="https://www.youtube.com/embed/us2bq5vpQ9g" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>'

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
