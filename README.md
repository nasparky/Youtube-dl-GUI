# Youtube-dl-GUI
GUI made for the youtube_dl  module using pyqt5

So this is technically still a Work in progress type of project to do, however I haven't gotten to the realization that this 
GUI in particular lacks some of the necessary functionality such as using FFPMEG for audio conversion already assigned through the Qt library.
This file does require that you have the FFPMEG Executable in your scripts directory as the module Youtube_DL is has an executable already in that same directory which requires this codec for mp3 conversion.

Anyways here is the GUI for use, it provides a Queue specifically designed to work with batch loading and allows the ability to specfify the type
whether it would be an audio or video file. This is not designed to spec as the options are just radio buttons. It also includes a terminal to
be able to see where things went wrong and the general background logic going through. Another feature that is includes is the abliity to see a preview 
actual link itself in HTML iframe framework which works pretty decently whenever a new link is added to the queue.


![Screenshot 2021-05-21 134502](https://user-images.githubusercontent.com/8619943/119177755-c3c0e400-ba3a-11eb-9d83-72c0b8ab548c.png)

The file is actually not completely complete, however most of the functionality is there and the use of it needs work.
