#!/bin/python

# credit to https://ryan.himmelwright.net/post/gnome-font-scaling-script/ for the bash script this is based on

import os, gi, requests, time, signal, subprocess, re
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator, Notify as notify, GLib as glib
from PIL import Image, ImageDraw as Draw, ImageFont as Font
from pynput import keyboard


class Tray:
    def __init__(self):

        # create scales
        self.scales = [1.0, 1.25, 1.5]

        # create icons for each scale
        for scale in self.scales:
            text = f"{scale}"
            size = (96,64)
            font_size = 36
            image = Image.new('RGBA', size, (255, 255, 255, 0))
            draw = Draw.Draw(image)
            try:
                font = Font.truetype("DejaVuSans-Bold.ttf", font_size)
            except IOError:
                font = Font.load_default()
            text_size = draw.textsize(text, font=font)
            text_position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
            draw.text(text_position, text, font=font, fill=(255, 255, 255, 255))

            # Save the image to a temporary file
            temp_icon = f'/tmp/tray_{scale}_icon.png'
            image.save(temp_icon)


        # initiate tray app
        self.indicator = appindicator.Indicator.new("fontscale", "", appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        # create menu based on state
        self.update_icon()
        self.menu()
    
        # keyboard shortcut to cycle through scales
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<shift>+m': self.toggle_scale
        })
        self.listener.start()
        

    def update_icon(self):
        ## Generate an image with the given text
        #text = f"{text}"
        #print(text)
        #size = (96,64)
        ##size = (64, 64)
        #font_size = 42
        #image = Image.new('RGBA', size, (255, 255, 255, 0))
        #draw = Draw.Draw(image)
        #try:
        #    font = Font.truetype("DejaVuSans-Bold.ttf", font_size)
        #except IOError:
        #    font = Font.load_default()
        #text_size = draw.textsize(text, font=font)
        #text_position = ((size[0] - text_size[0]) // 2, (size[1] - text_size[1]) // 2)
        #draw.text(text_position, text, font=font, fill=(255, 255, 255, 255))

        ## Save the image to a temporary file
        #temp_icon = '/tmp/tray_icon.png'
        #image.save(temp_icon)


        # Set the generated image as the tray icon
        #self.indicator.set_icon_full(temp_icon, text)
        self.get_scale()
        self.indicator.set_icon_full(f"/tmp/tray_{self.scale}_icon.png", f"{self.scale}")


    def menu(self):
        menu = gtk.Menu()

        # add font scales as menu options
        #scales = [1.0, 1.25, 1.5]
        connections = {}
        #for scale in scales:
        for scale in self.scales:
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
        subprocess.Popen(["gsettings","set","org.gnome.desktop.interface","text-scaling-factor", f"{scale}"])
        time.sleep(0.3)
        self.update_icon()
        #print('a')
        #print(self.scale)
        #glib.timeout_add(200, self.update_icon, self.scale)
        #print('b')


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
