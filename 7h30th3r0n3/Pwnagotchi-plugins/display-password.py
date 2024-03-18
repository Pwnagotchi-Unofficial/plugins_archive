import time
import subprocess
from pwnagotchi.ui.components import LabeledValue
from pwnagotchi.ui.view import BLACK
import pwnagotchi.ui.fonts as fonts
import pwnagotchi.plugins as plugins
import logging
import pwnagotchi
import os


class DisplayPassword(plugins.Plugin):
    __Original_author__ = '@nagy_craig'
    __Modified__ = '@7h30th3r0n3'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'A plugin to display recently cracked and fail passwords'
    last_update_time = 0

    def on_loaded(self):
        logging.info("[display-password] loaded")

    def on_ui_setup(self, ui):
        ui.add_element('display-password', LabeledValue(color=BLACK, label="", value='', position=(ui.width() // 2 - 10, 76), label_font=fonts.Bold, text_font=fonts.Small))
        ui.add_element('display-password-fail', LabeledValue(color=BLACK, label="", value='', position=(0, 32), label_font=fonts.Bold, text_font=fonts.Small))

    def on_unload(self, ui):
        with ui._lock:
            ui.remove_element('display-password')
            ui.remove_element('display-password-fail')

    def on_ui_update(self, ui):
        current_time = time.time()
        if current_time - self.last_update_time < 10:
            return  # Skip update if less than 10 seconds since last update
        self.last_update_time = current_time

        # Update password display
        try:
            with open('/home/pi/wpa-sec.cracked.potfile', 'r') as f:
                last_line = os.popen('tail -n 1 /home/pi/wpa-sec.cracked.potfile').read().strip()
                if last_line:
                    ssidname, pwd = last_line.split(" - ")
                    ui.set('display-password-fail', "{} - {}".format(ssidname, pwd))
                else:
                    ui.set('display-password', "   Aucun crack...")
                matching_line = next((line.strip() for line in subprocess.check_output(['tac', '/home/pi/wpa-sec.cracked.potfile']).decode().split('\n') if "FAIL" not in line), None)
                if matching_line:
                    ssidname, pwd = matching_line.split(" - ")
                    ui.set('display-password', "{} - {}".format(ssidname, pwd))
                else:
                    ui.set('display-password', "Aucun mdp crack...")
        except FileNotFoundError:
            logging.warning("File not found: /home/pi/wpa-sec.cracked.potfile")
            ui.set('display-password', "   Aucun crack...")