import os
import sys
from cx_Freeze import setup, Executable

workerFile = os.path.join(os.getcwd(), "worker.py")
extraFile = os.path.join(os.getcwd(), "extras.py")
ydlFile = os.path.join(os.getcwd(), "ydl.py")
styleFile = os.path.join(os.getcwd(), "stylesheet.py")

additional_modules = []
build_exe_options = {"includes": additional_modules,
                     "packages": ["PyQt6"],
                     "excludes": ["tkinter", "sqlite3", "PyQt6.QtNetwork",
                                  "PyQt6.QtScript"],
                     "include_files": ["favicon.ico", workerFile, extraFile,
                                       ydlFile, styleFile, "ffmpeg.exe"],
                     "optimize": 2}

base = None
if sys.platform == "win32":
  base = "Win32GUI"

setup(name="ydl",
      version="1.0",
      description="Youtube Video Downloader",
      options={"build_exe": build_exe_options},
      executables=[Executable(script="gui.py", base=base)])