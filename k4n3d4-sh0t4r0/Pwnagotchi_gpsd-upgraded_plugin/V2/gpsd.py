# Based on the GPS plugin from https://github.com/kellertk/pwnagotchi-plugin-gpsd
# Based itself on the GPS plugin from https://github.com/evilsocket
#
# Requires https://github.com/MartijnBraam/gpsd-py3
import json
import logging
import os
import pwnagotchi.plugins as plugins
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi
import gpsd

class GPSD:
    def __init__(self, gpsdhost, gpsdport):
        gpsd.connect(host=gpsdhost, port=gpsdport)
        self.running = True
        self.coords = {
            "Latitude": None,
            "Longitude": None,
            "Altitude": None,
            "Date": None
        }

    def update_gps(self):
        if self.running:
            packet = gpsd.get_current()
            if packet.mode >= 2:
                    self.coords = {
                        "Latitude": packet.lat,
                        "Longitude": packet.lon,
                        "Altitude": packet.alt if packet.mode > 2 else None,
                        "Date": packet.time
                    }
        return self.coords

class gpsd_coord(plugins.Plugin):
    __author__ = "k4n3d4_sht4r0@proton.me"
    __version__ = "1.0.0"
    __license__ = "GPL3"
    __description__ = "Save gpsd coordinates to an external file"

    def __init__(self):
        self.gpsd = None
        self.old_coords = None

    def on_loaded(self):
        self.gpsd = GPSD(self.options['gpsdhost'], self.options['gpsdport'])
        logging.info("[gpsd] plugin loaded")

    def on_ready(self, agent):
        if os.path.isfile(self.options['filelocation']) :
            with open(self.options['filelocation'], 'r') as f:
                self.old_coords = json.load(f)
            f.close()
            logging.info("[gpsd] last session gps position loaded")
        if (self.options["gpsdhost"]):
            logging.info(f"enabling bettercap's gps module for {self.options['gpsdhost']}:{self.options['gpsdport']}")
            try:
                agent.run("gps off")
            except Exception:
                logging.info(f"bettercap gps was already off")
                pass

            agent.run("set gps.device 127.0.0.1:2947; set gps.baudrate 9600; gps on")
            logging.info("bettercap set and on")
            self.running = True
        else:
            logging.warning("no GPS detected")

    def on_handshake(self, agent, filename, access_point, client_station):
        if self.old_coords :
            gps_filename = filename.replace(".pcap", ".gps.json")
            logging.info(f"[gpsd] saving GPS to {gps_filename} ({self.old_coords})")
            with open(gps_filename, "w+t") as fp:
                json.dump(self.old_coords, fp)
        else:
            logging.info("[gpsd] not saving GPS: no fix")

    def on_ui_setup(self, ui):
        # add coordinates for other displays
        if ui.is_waveshare_v4():
            lat_pos = (137, 75)
            lon_pos = (132, 84)
            alt_pos = (137, 94)
        elif ui.is_waveshare_v3():
            lat_pos = (137, 75)
            lon_pos = (132, 84)
            alt_pos = (137, 94)
        elif ui.is_waveshare_v1():
            lat_pos = (130, 70)
            lon_pos = (125, 80)
            alt_pos = (130, 90)
        elif ui.is_inky():
            lat_pos = (127, 60)
            lon_pos = (127, 70)
            alt_pos = (127, 80)
        elif ui.is_waveshare144lcd():
            # guessed values, add tested ones if you can
            lat_pos = (67, 73)
            lon_pos = (62, 83)
            alt_pos = (67, 93)
        elif ui.is_dfrobot_v2:
            lat_pos = (127, 75)
            lon_pos = (122, 84)
            alt_pos = (127, 94)
        elif ui.is_waveshare27inch():
            lat_pos = (6,120)
            lon_pos = (1,135)
            alt_pos = (6,150)
        else:
            # guessed values, add tested ones if you can
            lat_pos = (127, 51)
            lon_pos = (127, 56)
            alt_pos = (102, 71)

        label_spacing = 0

        ui.add_element(
            "latitude",
            LabeledValue(
                color=BLACK,
                label="lat:",
                value="-",
                position=lat_pos,
                label_font=fonts.Small,
                text_font=fonts.Small,
                label_spacing=label_spacing,
            ),
        )
        ui.add_element(
            "longitude",
            LabeledValue(
                color=BLACK,
                label="long:",
                value="-",
                position=lon_pos,
                label_font=fonts.Small,
                text_font=fonts.Small,
                label_spacing=label_spacing,
            ),
        )
        ui.add_element(
            "altitude",
            LabeledValue(
                color=BLACK,
                label="alt:",
                value="-",
                position=alt_pos,
                label_font=fonts.Small,
                text_font=fonts.Small,
                label_spacing=label_spacing,
            ),
        )

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('latitude')
            ui.remove_element('longitude')
            ui.remove_element('altitude')

    def on_ui_update(self, ui):
        coords = self.gpsd.update_gps()
        if coords and all([
            coords["Latitude"], coords["Longitude"]
        ]):
            self.old_coords = coords
            with open(self.options['filelocation'], 'w') as f:
                json.dump(self.old_coords, f)
            f.close()
        if self.old_coords :
            ui.set("latitude", f"{self.old_coords['Latitude']:.4f} ")
            ui.set("longitude", f" {self.old_coords['Longitude']:.4f} ")
            ui.set("altitude", f" {self.old_coords['Altitude']:.1f}m ")
