# pwnagotchi-plugins
Various homebrew pwnagotchi plugins for the pwnagotchi.

# basiclight Config.toml
1. Make sure you have created the custom folder and put it in `/etc/pwnagotchi/config.toml`, this can point to wherever you will put the plugins:
`main.custom_plugins = "/etc/pwnagotchi/custom"`

2. `main.plugins.basiclight.enabled = true`
   
## What it Does
basiclight.py accesses RPi02W's GPIO, pins are listed in the file, may want to change for your operation. For usage with: https://www.pishop.ca/product/pi-traffic-light/
