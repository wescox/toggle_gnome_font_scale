#!/bin/python

# credit to https://ryan.himmelwright.net/post/gnome-font-scaling-script/ for the bash script this is based on

import os, gi, requests, time, signal, subprocess, re
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, Notify as notify, GLib as glib
from PIL import Image as imaage, ImageDraw as draw


class Tray:
    def __init__(self):
        # initiate tray app
        self.indicator = appindicator.Indicator.new("fontscale", "", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # get initial state
        #self.set_state()

        # create menu based on state
        self.menu()
    

    def menu(self):
        menu = gtk.Menu()

        scales = [1.0, 1.25, 1.5]
        connections = {}
        for scale in scales:
            connections[scale] = gtk.MenuItem()
            connections[scale].set_label(f"{scale}")
            connections[scale].connect('activate', self.notify, scale)
            menu.append(connections[scale])

        scales_exit = gtk.MenuItem(label="Quit")
        scales_exit.connect('activate', self.quit)
        menu.append(scales_exit)

        menu.show_all()
        self.indicator.set_menu(menu)
    
        return menu
    

    #def set_state(self):


    def notify(self, _, message):
        subprocess.Popen(["notify-send", "ServiceTrade VPN", message]) 
    

    def quit(self,_):
        gtk.main_quit()
    

if __name__ == "__main__":
    
    # simply so that CTRL+C works if running from CLI
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = Tray()
    gtk.main()
