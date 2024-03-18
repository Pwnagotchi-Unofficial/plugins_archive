import logging
import os
from datetime import datetime
import pwnagotchi
import pwnagotchi.plugins as plugins
import xml.etree.ElementTree as ET

class WarwalkingTrailsKmlSingle(plugins.Plugin):
    __author__ = "https://github.com/JD-2006"
    __version__ = "1.1.0"
    __license__ = "GPL3"
    __description__ = """
    When enabled will log continuous positions based on epoch interval (1-2 mins) to a single KML file.
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
            logging.info("[warwalking_trails_kml_single] plugin loaded")
        except Exception as e:
            logging.error("warwalking_trails_kml_single.on_loaded: %s" % e)

    def on_ready(self, agent):
        try:
            self.gps = plugins.loaded["gps"]
            if not self.gps:
                logging.error("[warwalking_trails_kml_single] gps plugin not loaded!")
            else:
                # Create the KML file on plugin readiness if it doesn't exist
                self.create_kml_file()
        except Exception as e:
            logging.error(f"warwalking_trails_kml_single.on_ready: {e}")

    def create_kml_file(self):
        try:
            date_time_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            kml_filename = os.path.join(self.options['kml_path'], f"Trail-Single-{date_time_str}.kml")

            # Check if the KML file already exists
            if not os.path.exists(kml_filename):
                # Create KML file with the initial structure
                kml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <kml xmlns="http://www.opengis.net/kml/2.2">
                        <Document>
                            <!-- Placeholder for Placemarks -->
                        </Document>
                    </kml>"""

                with open(kml_filename, "w") as f:
                    f.write(kml_content)

                logging.info(f"KML file created: {kml_filename}")

            # Store the filename for future reference
            self.kml_filename = kml_filename

        except Exception as e:
            logging.error(f"warwalking_trails_kml_single.create_kml_file: {e}")

    def on_epoch(self, agent, epoch, data):
        try:
            if self.gps and self.gps.running:
                self.gps.coordinates = agent.session()["gps"]
        except Exception as e:
            logging.error(f"warwalking_trails_kml_single.on_epoch: {e}")

        try:
            if self.gps and self.gps.coordinates:
                coords = self.gps.coordinates
                if all([coords.get("Latitude"), coords.get("Longitude")]):
                    # Check if the KML file is already created
                    if not hasattr(self, 'kml_filename'):
                        self.create_kml_file()

                    # Open the existing KML file
                    tree = ET.parse(self.kml_filename)
                    root = tree.getroot()

                    # Define the KML namespace and register it
                    kml_namespace = "http://www.opengis.net/kml/2.2"
                    ET.register_namespace("", kml_namespace)

                    # Get the Document element or create it if not exists
                    document = root.find(".//{%s}Document" % kml_namespace)
                    if document is None:
                        document = ET.Element("{%s}Document" % kml_namespace)
                        root.append(document)

                    # Create a new Placemark for the current coordinates
                    new_placemark = ET.Element("{%s}Placemark" % kml_namespace)

                    # Add the name (date and time) to the Placemark
                    name = ET.Element("{%s}name" % kml_namespace)
                    name.text = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_placemark.append(name)

                    point = ET.Element("{%s}Point" % kml_namespace)
                    coordinates = ET.Element("{%s}coordinates" % kml_namespace)
                    coordinates.text = f"{coords['Longitude']},{coords['Latitude']},{coords['Altitude']}"
                    point.append(coordinates)
                    new_placemark.append(point)

                    # Append the new Placemark to the KML file
                    document.append(new_placemark)

                    # Save the modified KML file
                    tree.write(self.kml_filename, encoding="utf-8", xml_declaration=True, default_namespace="")

                    logging.info(f"KML file updated: {self.kml_filename}")

        except Exception as e:
            logging.error(f"warwalking_trails_kml_single.update_kml_file: {e}")
