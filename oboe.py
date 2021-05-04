#!/usr/bin/python3 -W ignore::DeprecationWarning
import gi
import mania.tidal
import mania.constants
import toml
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
        self.authcheck()


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

    def authcheck(self):
        # Check if client is authenticated by TIDAL
        try:
            with open(mania.constants.SESSION_PATH, "r") as session_file:
                session_dict = toml.load(session_file)
            self.session = mania.tidal.TidalSession(**session_dict)
            self.session.check_valid()
        # Authenticate
        except (FileNotFoundError, toml.TomlDecodeError, mania.tidal.TidalAuthError):
            self.session = mania.tidal.TidalSession()
            self.session.get_authorization()
            token = self.session.user_code
            os.system("notify-send 'Oboe' 'Please sign in to TIDAL' -i oboe")
            os.system("xdg-open https://link.tidal.com/" + token)
            self.session.authenticate()
            with open(mania.constants.SESSION_PATH, "w") as session_file:
                toml.dump(self.session.to_dict(), session_file)


win = Oboe()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()