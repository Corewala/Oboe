#!/usr/bin/python3 -W ignore::DeprecationWarning
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Oboe(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title ="Oboe")
        Gtk.Window.set_resizable(self, False)
        self.set_border_width(10)
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 20)
        self.add(self.box)
        # create TIDAL area
        self.tidalentry = Gtk.Entry()
        tidalbutton = Gtk.Button(label = "Download")
        tidalbutton.connect("clicked", self.download)
        self.box.pack_start(self.tidalentry, True, True, 0)
        self.box.pack_start(tidalbutton, True, True, 0)


    def download(self, widget):
        # run mania
        commandstatus = os.system("mania url " + self.tidalentry.get_text() + " --output-directory ~/Music")
        if not commandstatus:
            os.system("notify-send 'Oboe' 'Track downloaded' -i oboe")
            print("\33[92m" + "Track downloaded" + "\33[0m")
        elif int(commandstatus) == 512 or int(commandstatus) == 256:
            os.system("notify-send 'Oboe' 'Please use a real TIDAL URL' -u critical -i oboe")
            print("\33[33m" + "Please use a real TIDAL URL" + "\33[0m")
        else:
            os.system("notify-send 'Oboe' 'Failed to download track' -u critical -i oboe")
            print("\33[31m" + "Failed to download track" + "\33[0m")


win = Oboe()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()