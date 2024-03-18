# pwnagotchi-plugin-gpsd
a plugin for [pwnagotchi](pwnagotchi.ai) that shows your GPS location from [GPSD](https://gpsd.gitlab.io/gpsd/index.html)

## Why?
[Bettercap](https://www.bettercap.org/modules/utils/gps/) has built in support for GPS devices, and this is how the [pwnagotchi gps module](https://github.com/evilsocket/pwnagotchi/blob/master/pwnagotchi/plugins/default/gps.py) gets location information. But Bettercap's GPS support is very bare-bones. By using GPSD we get all of the nice features that GSPD adds:
* GPS setup and polling earlier in the boot process.
* More knobs and switches for configuring your GPS.
* [Odd device support](https://gpsd.gitlab.io/gpsd/hardware.html).
* **Multiple application support**. Your GPS can supply data to pwnagotchi, `chrony`, `gpsmon`, and any other app you want at the same time
* GPS hotplugging.

## Requirements
On top of pwnagotchi, you'll need a configured (and tested working!) `gpsd`, and also `gpsd-py3`.

As an example:
```bash
pi@pwnagotchi:~ $ sudo apt install gpsd gpsd-clients
pi@pwnagotchi:~ $ sudo pip3 install gpsd-py3
pi@pwnagotchi:~ $ sudo bash -c 'cat > /etc/default/gpsd' << EOF
# Default settings for the gpsd init script and the hotplug wrapper.

# Start the gpsd daemon automatically at boot time
START_DAEMON="true"

# Use USB hotplugging to add new USB devices automatically to the daemon
USBAUTO="false"

# Devices gpsd should collect to at boot time.
# They need to be read/writeable, either by user gpsd or the group dialout.
DEVICES="/dev/ttyS0"
# or, if you want to setup with BlueNMEA on your android phone, with bt-tethering :
# DEVICES="tcp://192.168.44.1:4352"

# Other options you want to pass to gpsd
GPSD_OPTIONS="-n"
EOF
pi@pwnagotchi:~ $ sudo systemctl enable gpsd.service
pi@pwnagotchi:~ $ sudo systemctl start gpsd.service
pi@pwnagotchi:~ $ sudo mkdir -p /usr/local/share/pwnagotchi/installed-plugins/
```

Test out your GPS with `gpsmon`. These are generic instructions for setting up and testing GPSD, you may need to do something differently.

## Setup
In `config.toml`, set
```
main.custom_plugins = "/usr/local/share/pwnagotchi/installed-plugins/"
main.plugins.gpsd.enabled = true
main.plugins.gpsd.gpsdhost = "127.0.0.1"
main.plugins.gpsd.gpsdport = 2947
```

Place gpsd.py in `/usr/local/share/pwnagotchi/installed-plugins`

## Finished!

Here's what it looks like. Sort of.
![Front image of pwnagotchi](https://i.imgur.com/3aVdWFQ.jpg)

Here's the GPS on the back.
![Back image of pwnagotchi](https://i.imgur.com/LdJQ9UH.jpg)
