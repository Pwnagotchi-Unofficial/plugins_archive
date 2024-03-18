import time
import logging
import os
from gpiozero import LED
import pwnagotchi.plugins as plugins

class GPS(plugins.Plugin):
    __author__ = "https://github.com/JD-2006"
    __version__ = "1.0.0"
    __license__ = "GPL3"
    __description__ = "Flash LED on GPIO 26 when there is GPS data."

    def __init__(self):
        self.running = False
        self.coordinates = None
        self.options = dict()
        self.led = LED(26)  # Initialize LED on GPIO 26

    def on_loaded(self):
        logging.info(f"gps_led plugin loaded")

    def on_ready(self, agent):
        if os.path.exists(self.options["device"]) or ":" in self.options["device"]:
            logging.info(f"enabling gps_led module for {self.options['device']}")
            try:
                agent.run("gps off")
            except Exception:
                logging.info(f"gps_led module was already off")
                pass

            agent.run(f"set gps.device {self.options['device']}")
            agent.run(f"set gps.baudrate {self.options['speed']}")
            agent.run("gps on")
            logging.info(f"gps_led module enabled on {self.options['device']}")
            self.running = True
        else:
            logging.warning("gps_led no GPS detected")

    def on_ui_update(self, ui):
        try:
            self.led.blink(0.5, 5)
        except Exception as e:
            logging.error(f"gps_led An error occurred: {e}")
