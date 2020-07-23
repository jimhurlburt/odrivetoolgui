This readme is for odrivetoolgui

As the name suggests, the immediate goal is to
make a gui interface for the current version of
odrivetool.

At some time in the future the scope may expand,
but in the short run I won't entertain anything
beyond odrivetool and liveplotter.

At this writing I can't guarantee that it will run
on anything but kubuntu 18.4 and raspberry pi.  I
would expect it to run on windows10 and mac, but
haven't tried it yet on windows and don't have a
mac to test with.

findany will work with a usb connection.
findonport won't work on anything but a pi with a
serial wire from the gpio pins.  Making this
better is on the todo list, but not at the top.

Other than that, I have a very limited subset of
odrivetool working and will add more frequently.

It is written in python3 with pyqt. 

If your setup will run odrivetool at the command
line and you have pip3 installed --

For linux and the pi
pip3 install --user pyqt5  
sudo apt-get install python3-pyqt5  
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools

The pip3 line throws an error but at least on my
two boxes, after running them

python3
import PyQt5

works.

When I have things running to suit in linux I will
test in windows and add to this file.

There are 4 files in the repository.  
readme.txt (this file)
odrive_tool.ui  (the qt designer file)

ui_odrive.py (generated by pyuic5.  This file
should not be modified directly.  If it is all
changes will be lost when pyuic5 is run next time)

odrivetoolgui.py  (python3 odrivetoolgui.py to run)

Comments and suggestions that are within the scope
described above are welcome.  Python developers
are encouraged to participate.

Jim Hurlburt
Bend, OR USA
hurlburtjl@gmail.com



