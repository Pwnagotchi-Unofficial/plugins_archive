# PiSugar 2 Plugin for Pwnagotchi (built-in dependencies)
# From <https://github.com/tisboyo/pwnagotchi-pisugar2-plugin>

# Maintainer: mochaaP <self@mochaa.ws>

### start <pisugar2.py> ###
# Written by Tisboyo - 10230718+tisboyo@users.noreply.github.com

# Used for interacting with the PiSugar2 from
# https://www.tindie.com/products/pisugar/pisugar2-battery-for-raspberry-pi-zero/
# Does require installing the PiSugar-Power-Manager software per PiSugars instructions

# This library connects over tcp using a netcat like interaction
# and supports all of the currently published commands.

from __future__ import annotations
import socket
from collections import namedtuple
from datetime import datetime

class Netcat:

    """ Python 'netcat like' module """

    # Graciously borrowed from https://gist.github.com/leonjza/f35a7252babdf77c8421

    def __init__(self, ip: str, port: int):

        self.buff = ""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((ip, port))

    def read(self, length: int = 1024) -> str:

        """ Read 1024 bytes off the socket """

        # Decode the returned byte string to a string and strip trailing whitespace
        return self.socket.recv(length).decode("UTF-8").rstrip()

    # Not currently used
    # def read_until(self, data):

    #     """ Read data into the buffer until we have data """

    #     while not data in self.buff:
    #         self.buff += self.socket.recv(1024)

    #     pos = self.buff.find(data)
    #     rval = self.buff[: pos + len(data)]
    #     self.buff = self.buff[pos + len(data) :]

    #     return rval

    def write(self, data: str) -> None:

        data = data.encode("UTF-8")
        self.socket.send(data)

    def close(self) -> None:

        self.socket.close()

    def query(self, data: str) -> str:
        self.write(data)
        return self.read()


class InvalidRequest(Exception):
    pass


class PiSugar2:
    """Defaults to localhost on the default port but can specify ip and port"""

    def __init__(self, ip="127.0.0.1", port=8423):
        self.netcat = Netcat(ip, port)
        self._model = None

        # Create a named tuple
        self.nt_values = namedtuple("PiSugar2", "name value command")

    def _is_float(self, value):
        # Check if a value passed is a float
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _nt(self, output: bytes, name: str = None) -> namedtuple:
        """
        Converts the provided values into a named tuple:
            .name    = Name of the value
            .value   = Value
            .command = Command used to request informatino
        """

        # Check to make sure the request was valid
        if output == "Invalid request.":
            raise InvalidRequest

        # Split the values received into name and value
        tup = tuple(output.split(": ", 1))

        # Set name to default if one not passed
        if not name or name == "":
            name = tup[0]

        # Set the value
        if tup[1] == "false":
            value = False
        elif tup[1] == "true":
            value = True
        elif tup[1].isnumeric():
            # A numeric value
            value = int(tup[1])
        elif self._is_float(tup[1]):
            value = float(tup[1])
        else:
            try:
                # If the return is a datetime object
                value = datetime.fromisoformat(tup[1])
            except ValueError:
                # A string value
                value = tup[1]

        # Assign them to a named tuple of .name and .value
        values = self.nt_values(name=name, value=value, command=tup[0])

        return values

    def get_model(self) -> namedtuple:
        """Returns the currently installed model number"""
        # model: PiSugar 2 (4-LEDs)
        # https://github.com/PiSugar/pisugar-power-manager-rs/blob/366ea0ca30ed88ffcf90dfe7c3092a74d97e02cc/pisugar-server/src/main.rs#L69
        if not self.model:
            # If we've already checked the model once, it hasn't changed.
            output = self.netcat.query("get model")

            self._model = self._nt(output)

        return self._model

    def get_battery_percentage(self) -> namedtuple:
        """Returns the current battery level percentage"""
        # battery: 84.52326
        output = self.netcat.query("get battery")
        return self._nt(output, "percentage")

    def get_voltage(self) -> namedtuple:
        """Returns the current battery voltage"""
        # battery_v: 4.0150776
        output = self.netcat.query("get battery_v")
        return self._nt(output, "voltage")

    def get_amperage(self) -> namedtuple:
        """Returns the current battery amperage draw"""
        # battery_i: 0.0040908856
        output = self.netcat.query("get battery_i")

        return self._nt(output, "amps")

    def get_charging_status(self) -> namedtuple:
        """Returns if the battery is currently charging"""
        # battery_charging: false
        output = self.netcat.query("get battery_charging")

        return self._nt(output, "charging")

    def get_time(self) -> namedtuple:
        """Returns the time value with a datetime object as .value"""
        # rtc_time: 2020-07-17T01:44:20+01:00
        output = self.netcat.query("get rtc_time")

        return self._nt(output, "time")

    def get_alarm_enabled(self) -> namedtuple:
        """Returns the status of alarm enable"""
        # rtc_alarm_enabled: false
        output = self.netcat.query("get rtc_alarm_enabled")

        return self._nt(output, "alarm_enabled")

    def get_alarm_time(self) -> namedtuple:
        """Returns the time the alarm is set for"""
        output = self.netcat.query("get rtc_alarm_time")

        return self._nt(output, "alarm_time")

    def get_alarm_repeat(self) -> namedtuple:
        """Returns alarm repeat value"""
        output = self.netcat.query("get alarm_repeat")
        return self._nt(output)

    def get_button_enable(self, press: str) -> namedtuple:
        """
        Returns the status of enabled buttons
        press = "single", "double", or "long"
        """
        if press.lower() in ["single", "double", "long"]:
            output = self.netcat.query(f"get button_enable {press}")
            nt = namedtuple("ButtonEnable", "name value command")

            value = True if output.split(" ")[2] == "true" else False

            return nt(f"button_enable_{press}", value, "button_enable")
        else:
            raise InvalidRequest

    def get_button_shell(self, press: str) -> namedtuple:
        """
        Returns the script for when a button is clicked
        press = "single", "double", or "long"
        """
        if press.lower() in ["single", "double", "long"]:
            output = self.netcat.query(f"get button_shell {press}")
            # Use a custom namedtuple instead of the normal one, so we get to do all the work here
            nt = namedtuple("ButtonShell", "name value command shell")

            split = output.split(" ", 2)
            name = split[0]
            value = split[1]
            command = f"button_shell_{press}"

            try:
                shell = split[2]
            except IndexError:
                shell = None

            return nt(name, value, command, shell)
        else:
            raise InvalidRequest

    def get_safe_shutdown_level(self) -> namedtuple:
        """Returns the safe shutdown level in percentage of battery"""
        output = self.netcat.query("get safe_shutdown_level")
        return self._nt(output)

    def get_battery_allow_charging(self) -> namedtuple:
        """Returns whether the charging usb is plugged (new model only)"""
        output = self.netcat.query("get battery_allow_charging")
        return self._nt(output)

    def get_battery_power_plugged(self) -> namedtuple:
        """Returns whether the charging usb is plugged (new model only)"""
        output = self.netcat.query("get battery_power_plugged")
        return self._nt(output)

    def get_battery_led_amount(self) -> namedtuple:
        """Returns the charging indicate led amount, 4 for old model, 2 for new model"""
        output = self.netcat.query("get battery_led_amount")
        return self._nt(output)

    def get_safe_shutdown_delay(self) -> namedtuple:
        """Returns the safe shutdown delay in seconds"""
        output = self.netcat.query("get safe_shutdown_delay")
        return self._nt(output)

    def set_rtc_from_pi(self) -> namedtuple:
        """Sets the RTC to the current time on the Pi"""
        output = self.netcat.query("rtc_pi2rtc")
        return self._nt(output)

    def set_pi_from_rtc(self) -> namedtuple:  # Upstream not working
        """Sets the Pi clock to the RTC value"""
        output = self.netcat.query("rtc_rtc2pi")
        return self._nt(output)

    def set_time_from_web(self) -> namedtuple:
        # Not working (may depend on systemd-timesyncd.service )
        """Sets the RTC and Pi clock from the web"""
        output = self.netcat.query("rtc_web")
        return self._nt(output)

    def set_rtc_alarm(
        self, time: datetime.datetime, repeat: list = [0, 0, 0, 0, 0, 0, 0]
    ) -> namedtuple:
        """Sets the alarm time
        time = datetime.datetime object
        repeat = list(0,0,0,0,0,0,0) with each value being 0 or 1 for Sunday-Saturday
        """

        timestr = datetime.isoformat(time)

        if not datetime.utcoffset(time):
            timestr += "+00:00"

        # Build repeat string
        s = str()
        for x in repeat:
            # Only accept 0 or 1
            if x in [0, 1]:
                s += str(x)
            else:
                raise ValueError

        repeat_dec = int(s, 2)  # Convert the string to decimal from binary

        print(f"rtc_alarm_set {timestr} {repeat_dec}")
        output = self.netcat.query(f"rtc_alarm_set {timestr} {repeat_dec}")
        return self._nt(output)

    def disable_alarm(self) -> namedtuple:
        """Disable the RTC alarm"""
        output = self.netcat.query("rtc_alarm_disable")
        return self._nt(output)

    def set_button_enable(self, press: str, enable: bool = True) -> namedtuple:
        """
        Enables the button press
        press = single, double or long
        enable = True/False, defaults to True
        """

        if press.lower() in ["single", "double", "long"]:

            output = self.netcat.query(f"set_button_enable {press} {int(enable)}")
            return self._nt(output)

        else:
            raise InvalidRequest

    def set_button_shell(
        self, press: str, shell: str, enable: bool = True
    ) -> namedtuple:
        """
        Sets the shell command to run when the button is pressed
        press = single, double or long
        shell = shell command to run, "sudo shutdown now"
        enable = True/False/None to enable the command, defaults to True, None for no change.
        """

        if press.lower() in ["single", "double", "long"]:
            if enable is not None:
                self.netcat.query(f"set_button_enable {press} {int(enable)}")

            output = self.netcat.query(f"set_button_shell {press} {shell}")

            return self._nt(output)

        else:
            raise InvalidRequest

    def set_safe_shutdown_level(self, level: int):
        """Set the battery percentage safe shutdown level max: 30"""
        level = int(level)
        if level > 30 or level < 0:
            raise InvalidRequest

        output = self.netcat.query(f"set_safe_shutdown_level {level}")
        return self._nt(output)

    def set_safe_shutdown_delay(self, delay: int):
        """Set the battery safe shutdown delay in seconds max: 120"""
        delay = int(delay)
        if delay > 120 or delay < 0:
            raise InvalidRequest

        output = self.netcat.query(f"set_safe_shutdown_delay {delay}")
        return self._nt(output)
### end <pisugar2.py> ### 

### start <plugin.py> ###
# Gets status of Pisugar2 - requires installing the PiSugar-Power-Manager
# curl http://cdn.pisugar.com/release/Pisugar-power-manager.sh | sudo bash
#
# based on https://github.com/evilsocket/pwnagotchi/blob/master/pwnagotchi/plugins/default/ups_lite.py
# https://www.tindie.com/products/pisugar/pisugar2-battery-for-raspberry-pi-zero/
import logging

from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import pwnagotchi
import time

class PiSugar(plugins.Plugin):
    __author__ = "10230718+tisboyo@users.noreply.github.com"
    __version__ = "0.0.1"
    __license__ = "GPL3"
    __description__ = "A plugin that will add a voltage indicator for the PiSugar 2"

    def __init__(self):
        self.ps = None
        self.is_charging = False
        self.is_new_model = False

    def on_loaded(self):
        self.ps = PiSugar2()
        logging.info("[pisugar] plugin loaded.")

        if self.ps.get_battery_led_amount().value == 2:
            self.is_new_model = True
        else:
            self.is_new_model = False

        if self.options["sync_rtc_on_boot"]:
            self.ps.set_pi_from_rtc()

    def on_ui_setup(self, ui):
        ui.add_element(
            "bat",
            LabeledValue(
                color=BLACK,
                label="BAT",
                value="0%",
                position=(ui.width() / 2 + 15, 0),
                label_font=fonts.Bold,
                text_font=fonts.Medium,
            ),
        )

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element("bat")

    def on_ui_update(self, ui):
        capacity = int(self.ps.get_battery_percentage().value)

        # new model use battery_power_plugged & battery_allow_charging to detect real charging status
        if self.is_new_model:
            if self.ps.get_battery_power_plugged().value and self.ps.get_battery_allow_charging().value:
                if not self.is_charging:
                    ui.update(force=True, new_data={"status": "Power!! I can feel it!"})
                self.is_charging = True
            else:
                self.is_charging = False

        ui.set("bat", str(capacity) + ("+" if self.is_charging else "%"))

        if capacity <= self.options["shutdown"]:
            logging.info(
                f"[pisugar] Empty battery (<= {self.options['shutdown']}): shuting down"
            )
            ui.update(force=True, new_data={"status": "Battery exhausted, bye ..."})
            time.sleep(3)
            pwnagotchi.shutdown()
### end <plugin.py> ###
