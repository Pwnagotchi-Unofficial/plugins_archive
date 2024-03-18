import logging
import os
from datetime import datetime
import pwnagotchi
import pwnagotchi.plugins as plugins

class WarwalkingTrailsKML(plugins.Plugin):
    __author__ = "https://github.com/JD-2006"
    __version__ = "1.1.0"
    __license__ = "GPL3"
    __description__ = """
    When enabled will log position based on epoch interval (1-2 mins) to a KML file.
    Requires gps plugin enabled.
    """

    __defaults__ = {
        'enabled': False,
        'kml_path': '/home/pi/',  # Set a default path for KML files
    }

    def __init__(self):
        self.ready = False
        self.gps = None

    def on_loaded(self):
        try:
            logging.info("[warwalking_trails_kml] plugin loaded")
        except Exception as e:
            logging.error("warwalking_trails_kml.on_loaded: %s" % e)

    def on_ready(self, agent):
        try:
            self.gps = plugins.loaded["gps"]
            if not self.gps:
                logging.error("[warwalking_trails_kml] gps plugin not loaded!")
        except Exception as e:
            logging.error(f"warwalking_trails_kml.on_ready: {e}")

    def on_epoch(self, agent, epoch, data):
        try:
            if self.gps and self.gps.running:
                self.gps.coordinates = agent.session()["gps"]
        except Exception as e:
            logging.error(f"warwalking_trails_kml.on_epoch: {e}")

        try:
            if self.gps and self.gps.coordinates:
                coords = self.gps.coordinates
                if all([coords.get("Latitude"), coords.get("Longitude")]):
                    date_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    kml_filename = os.path.join(self.options['kml_path'], f"Trail-{date_time_str}.kml")

                    # Create KML feature
                    kml_content = f"""<?xml version="1.0" ?>
                        <kml>
                            <Placemark>
                                <name>{date_time_str}</name>
                                <Point>
                                    <coordinates>{coords['Longitude']},{coords['Latitude']},{coords['Altitude']}</coordinates>
                                </Point>
                            </Placemark>
                        </kml>"""

                    # Save KML file
                    with open(kml_filename, "w") as f:
                        f.write(kml_content)

                    logging.info(f"KML file updated: {kml_filename}")
        except Exception as e:
            logging.error(f"warwalking_trails_kml.update_kml_file: {e}")
