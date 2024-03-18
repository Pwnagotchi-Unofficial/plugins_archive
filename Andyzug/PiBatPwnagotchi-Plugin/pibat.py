# Based on PiBat i2c version from https://github.com/Andyzug/PiBat
# and https://github.com/evilsocket/pwnagotchi/blob/master/pwnagotchi/plugins/default/ups_lite.py
# 
# functions for get PiBat status - needs enable "i2c" in raspi-config
#
# https://www.ebay.com/itm/264569479508

import struct

from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import smbus

full=4.05
empty=3.26
# TODO: add enable switch in config.yml an cleanup all to the best place
class UPS:
    VINmax = 5.1
    bus = smbus.SMBus(1)
    def __init__(self, address = 0x4D):
        self.address = address

    def readRaw(self):
        try:
            # Reads word (16 bits) as int
            rd = self.bus.read_word_data(self.address, 0)
            # Exchanges high and low bytes
            data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
            # Ignores two least significiant bits
            return data >> 2
        except:
            return 1

    def getValue(self):
        try:
            return float(self.VINmax) * self.readRaw() / 1023.0
        except:
            return 0.0

    def voltage(self):
        try:
            i=0
            tmp=0
            voltage = 0
            for x in range(50):
                tmp = self.getValue()
                voltage =voltage + tmp
               
            return voltage/50;

        except:
            return 0.0

    def capacity(self):
        try:
            lvl= ((self.voltage() - empty) * 100) / (full - empty)
            if lvl>100: # when charging this value can be more than 100% that's why we use this 'if'
                return 100
            else:
                return lvl
        except:
            return 0.0


class UPSLite(plugins.Plugin):
    __author__ = 'Andy'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin that will add a voltage indicator for the PiBat i2c Version'

    def __init__(self):
        self.ups = None

    def on_loaded(self):
        self.ups = UPS()

    def on_ui_setup(self, ui):
        ui.add_element('ups', LabeledValue(color=BLACK, label='Bat', value='', position=(ui.width() / 2 + 15, 0),
                                           label_font=fonts.Bold, text_font=fonts.Medium))

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('ups')

    def on_ui_update(self, ui):
        ui.set('ups', "%2i%%" % self.ups.capacity())