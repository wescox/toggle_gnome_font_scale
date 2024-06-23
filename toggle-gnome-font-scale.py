#!/bin/python

# credit to https://ryan.himmelwright.net/post/gnome-font-scaling-script/ for the bash script this is based on

import os, gi, requests, time, signal, subprocess, re
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, Notify as notify, GLib as glib
from PIL import Image as imaage, ImageDraw as draw
from pynput import keyboard


class Tray:
    def __init__(self):
        # initiate tray app
        self.indicator = appindicator.Indicator.new("fontscale", "", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # get initial state
        self.get_scale()

        # create menu based on state
        self.menu()
    
        # keyboard shortcut to cycle through scales
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+m': self.toggle_scale
        })
        self.listener.start()
        

    def menu(self):
        menu = gtk.Menu()

        # add font scales as menu options
        scales = [1.0, 1.25, 1.5]
        connections = {}
        for scale in scales:
            connections[scale] = gtk.MenuItem()
            connections[scale].set_label(f"{scale}")
            connections[scale].connect('activate', self.set_scale, scale)
            menu.append(connections[scale])

        # add separator
        separator = gtk.SeparatorMenuItem()
        menu.append(separator)

        # add quit option
        scales_exit = gtk.MenuItem(label="Quit")
        scales_exit.connect('activate', self.quit)
        menu.append(scales_exit)

        # build menu
        menu.show_all()
        self.indicator.set_menu(menu)
    
        return menu
    

    def get_scale(self):
        #output = subprocess.Popen(["gsettings","get","org.gnome.desktop.interface","text-scaling-factor"])
        output = subprocess.getoutput("gsettings get org.gnome.desktop.interface text-scaling-factor")
        self.scale = float(output.rstrip())


    def set_scale(self, _, scale):
        self.scale = subprocess.Popen(["gsettings","set","org.gnome.desktop.interface","text-scaling-factor", f"{scale}"])
        time.sleep(0.5)
        self.get_scale()


    def toggle_scale(self):
        if(self.scale == 1.5):
            scale = 1.0
        else:
            scale = self.scale + 0.25
        self.set_scale({}, scale)


    def quit(self,_):
        gtk.main_quit()
        self.listener.stop()
    

if __name__ == "__main__":
    
    # simply so that CTRL+C works if running from CLI
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = Tray()
    gtk.main()
