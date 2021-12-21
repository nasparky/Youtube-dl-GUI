# Updated version of the previously made one with additional cleanup
import os
import re
import subprocess
import traceback
import yt_dlp as yt

class Logger:
  def __init__(self, logger):
    self.logger = logger
  def debug(self, msg):
    pass
    #self.logger.emit(msg)
  def info(self, msg):
    pass
    #self.logger.emit(msg)
  def warning(self, msg):
    pass
    #self.logger.emit(msg)
  def error(self, msg):
    self.logger.emit(msg)

# Create a download format and use
def download(link_address, conversion_type, isPlaylist, progress_hook, logger):
  type = ""
  postprocess = {
    'key': 'FFmpegMetadata',
    'add_metadata': True
  }
  playlist = None
  if isPlaylist == "True":
    playlist = False
  else:
    playlist = True
  try:
    # Check for audio or video type
    if conversion_type == "Audio":
      type = "bestaudio/bestaudio[ext=m4a]/best"
    elif conversion_type == "Video":
      type = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    else:
      raise Exception("Incorrect information passed.")
    # Setup settings for ffmpeg
    ydl_opts = {
      'outtmpl': os.path.join(os.getcwd(), "Exports",
                  f"%(title)s.%(ext)s"),
      'format': type,
      'logger': Logger(logger),
      'prefer_ffmpeg': True,
      'ffmpeg_location': os.path.join(os.getcwd(), "ffmpeg.exe"),
      'noplaylist': playlist,
      'postprocessors': [postprocess],
      'progress_hooks': [progress_hook]
    }
    # Attempt to download video stream
    with yt.YoutubeDL(ydl_opts) as y:
      y.download(link_address)
  except Exception as e:
    logger.emit(str(traceback.format_exc()))

'''
def convert(filename, progress_hook):
  cmd = f"ffmpeg -i \"{os.path.join(os.getcwd(), 'Exports', filename)}.webm\" -y \"{os.path.join(os.getcwd(), 'Exports', filename)}.mp3\""
  process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,universal_newlines=True)
  duration = ""
  for line in process.stdout:
    if "DURATION" in line:
      s = ""
      matches = re.findall(r'[1-9]+')
      for match in matches:

      progress_hook({'status': 'downloading', 'filename': filename,
                     '_percent_str': }) # Mimic progress function
    if "size" in line:
      print(line)
  progress_hook({'status': "finished"})
'''