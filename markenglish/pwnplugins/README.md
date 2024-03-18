Dropbox api plugin for pwnagotchi.
Compatible with v1.5.3 and above which uses toml for configuration instead of yml 

# dropbox app console steps
Create an app for dropbox @ https://www.dropbox.com/developers/apps/create.

generate and copy app token from your app console.

copy the path/folder name.

# Steps to make this plugins work on pwnagotchi 1.5.3. and above using toml config
copy dropbox_ul.py to /home/pi/pwnplugins

edit main config.toml in pwnagotchi device with

main.custom_plugins = "/home/pi/pwnplugins"

main.plugins.dropbox_ul.enabled = true

main.plugins.dropbox_ul.app_token = "token generated in app console"

main.plugins.dropbox_ul.path = "/path or folder name made in app console"
