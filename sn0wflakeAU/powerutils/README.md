# Powerutils Pwnagotchi Plugin

The Powerutils plugin lets you run the Pwnagotchi's internal shutdown, restart, or reboot functions, instead of the system "shutdown" command. By using the internal functions, you can access other features such as syncing the AI data before shutdown, or switching between AUTO and MANU mode.

## Requirements

- A Raspberry Pi Zero W (RPi0w) with Pwnagotchi installed and running.
- A way of copying files on to the SD card; either by an SD card reader, or SSH over USB while the RPi0w is connected to a PC or laptop.

This *could* run on a Raspberry Pi Zero without the wireless (W), but we haven't tested it.

## Optional Parts

- Any compatible display, such as the [Waveshare e-ink display](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT) officially supported by the Pwnagotchi project.
- GPIO buttons to run the commands from
- or the [Pwnmenu Plugin](https://github.com/sn0wflakeAU/pwnmenu)

From here on, the complete working RPi0w with the Pwnagotchi system running on it will simply be referred to as "Pwnagotchi".

## How This Works

1. The file `powerutils.py` is loaded from the plugins directory.
3. At this point, `powerutils.py` waits in the background until it receives commands sent from the `powerutilscmd.py` script file.

## Installation

There are 2 files that need to be copied to the Pwnagotchi:

1. copy `powerutils.py` to `/usr/local/share/pwnagotchi/availaible-plugins/` (root access will be needed)
2. copy `powerutilscmd.py` to `/home/pi`

Edit the pwnagotchi configuration file with `sudo nano /etc/pwnagotchi/config.toml`

To enable contrib plugins (if you haven't already) add the following line if it doesn't exist yet:

```
main.custom_plugins = "/usr/local/share/pwnagotchi/available-plugins/"
```

Also, add the following line to enable the `powerutils` plugin:

```
main.plugins.powerutils.enabled = true
```

Save with **Ctrl+o** and exit with **Ctrl+x**. Then restart the Pwnagotchi service with:

```
sudo systemctl pwnagotchi restart
```

## Running power commands

The `/home/pi/powerutilscmd.py` script can accept the following commands:

- `shutdown` : Calls the `pwnagotchi.shutdown()` command to sync AI data and power down safely. If you have the Waveshare e-ink display, the pwnagotchi "face" will be asleep.
- `restart-auto` : Restarts the pwnagotchi service in **AUTO** mode, which starts scanning available networks for packets.
- `restart-manual` : Restarts the pwnagotchi service in **MANU** mode, useful for accessing the bettercap UI, or to use the RPi0's hardware for other features.
- `reboot-auto` : Same as **AUTO** mode above, but forces a system reboot.
- `reboot-manual` : Same as **MANU** mode above, but forces a system reboot.

### Examples

To shutdown the pwnagotchi safely, use:

```
python /home/pi/powerutilscmd.py shutdown
```

## Current issues

powerutils simply listens for the data 'shutdown' and 'restart-' or 'reboot-' variants on port 6799 without authentication of any kind. This could easily be triggered by anything that can send data to that port.

## License

This plugin is released under the GPLv3 license.


```
powerutils - A power management plugin for the pwnagotchi. Can be used with the pwnmenu plugin or on its own.
Copyright (C) 2024 Sam "sn0wflake" Allen <steampunkscientist1850@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
```
