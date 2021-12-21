# Qt5 worker class

import re
from ydl import download, convert
from PyQt6.QtCore import QObject, pyqtSignal

class QWorker(QObject):
  finished = pyqtSignal()
  progress = pyqtSignal(float, int)
  logger = pyqtSignal(str)

  def __init__(self, queue):
    super(QWorker, self).__init__()
    self.queue = queue
    self.filename = ""

  def run(self):
    try:
      initLength = len(self.queue)
      while len(self.queue) != 0: # Explicit :)
        data = self.queue.pop()
        self.logger.emit(f"Batch: {-1*len(self.queue)+initLength}/{initLength} - {data[1]}")
        download(data[1], data[2], data[3], self.__progress, self.logger)
        if data[2] == "Audio": # If the file needs to be converted
          convert(self.filename)
      self.finished.emit()
    except Exception as e:
      self.logger.emit(str(e))

  def __progress(self, d):
    if d['status'] == 'finished':
        self.progress.emit(-1*1.0, 0)
        self.filename = d['filename']
        matches = re.findall(r'[a-zA-Z0-9_]+', self.filename)
        self.filename = matches[len(matches)-2]
        print(self.filename)
    elif d['status'] == 'downloading':
        p = d['_percent_str']
        p.replace('%', '')
        p = re.findall(r'[0-9]+[.]+[0-9]+', p)
        if len(p) > 0:
          self.progress.emit(float(p[0]), d['eta'])
    else:
      self.logger.emit("Issue with progress hook, needs attention.")
  