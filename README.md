# Toggle GNOME font scale
A Linux tray applet to quickly change GNOME's font scale.  GNOME does not automatically adjust scale based on monitor resolution and changing the setting in the UI is cumbersome to manage if you have a laptop and change monitors often.  You can select from a scale of 1.0 (100%), 1.25 (125%), or 1.5 (150%).  You can also cycle through scales using ctrl + shift + m.  That shortcut can be easily changed in the code.  The tray icon will update to let you know which scale you are currently using.  This app manipulates "gsettings" which is specific to GNOME, however, other DEs may have a similar command that could be easily plugged into this code.

## Credit
This app was inspired by and largely based on a bash script posted on [ryan.himmelwright.net](https://ryan.himmelwright.net/post/gnome-font-scaling-script/).  
The icon I'm using for the app is provided by <a href="/">Freeimages.com</a>.  Feel free to change and use your own.  

## Installation

### Prequisties
 - Using GNOME DE
 - Install Python 3, pip, and the below packages:
    - [Pillow](https://python-pillow.org/):
        ```
        pip install pillow
        ```
    - pynput:
        ```
        pip install pynput
        ```

### Steps
Clone the repo.

Make the script executable
```bash
chmod u+x /path/to/toggle-gnome-font-scale.py
```

Symlink, move or copy the script.  I prefer symlinks.
```bash
ln -sf /path/to/toggle-gnome-font-scale.py $HOME/.local/bin
```
You will need to make $HOME/.local/bin if it does not exist and make sure it is in your PATH.  You could also use /usr/local/bin if you want the app to be available for all users.

Symlink, move, or copy the appropriate desktop file and icon.  I prefer symlinks.
```bash
ln -sf /path/to/toggle-gnome-font-scale.desktop $HOME/.local/share/applications
ln -sf /path/to/font_scale.png $HOME/.local/share/icons
```
Again, you could use the /usr/local versions of the above as well.

Finally, update your MIME type database
```bash
update-desktop-database $HOME/.local/share/applications
```
This doesn't work sometimes and you'll need to log out and back in to see changes take effect. I also have no idea if this command works in any DE other than GNOME.

## Issues
 - pynput monitors your keyboard and mouse input so it poses security concerns.  The purpose is to support cycling through the font scales with a keyboard shortcut.  If you're worried you can simply remove that functionality.  

