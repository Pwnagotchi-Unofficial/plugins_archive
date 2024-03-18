import re
import time
import logging
import subprocess
from pwnagotchi import plugins, config
from pwnagotchi.plugins import Plugin

class RestartPlugin(plugins.Plugin):
    __author__ = 'Discord: terminatoror'
    __version__ = '1.1.0'
    __license__ = 'GPL3'
    __description__ = 'This plugin restarts the pwnagotchi in case bettercap crashes. Heavily based on the restart scripts made by Discord: _dal_ '

    def __init__(self):
        super().__init__()

    def on_loaded(self):
        logging.info('RestartPlugin loaded...')
        #Ticker added to restart the entire device if needed
        self.running = True
        self.error_counts = {
            "concurrent_map": 0,
            "runtime": 0
        }
        self.threshold = 3
        self.ticker = 0
        self.ticker_limit = 3

        while self.running:
            self.search_log_for_errors()
            time.sleep(30)  # Search for errors every 30 seconds

    def search_string_in_log(self, search_string, log_file):
        try:
            with open(log_file, "r") as f:
                for line in f:
                    if re.search(search_string, line):
                        return True
        except Exception as e:
            logging.error(f"Error while searching log: {e}")
        return False

    def restart_device(self):
        logging.info("RestartPlugin: Restarting the device...")
        display.set('status', 'Error detected! Restarting...')
        subprocess.run("sudo reboot", shell=True)

    def search_log_for_errors(self):
        # Search for the first error message
        search_string_concurrent = "fatal error: concurrent map iteration and map write"
        log_file_concurrent = "/var/log/syslog"
        if self.search_string_in_log(search_string_concurrent, log_file_concurrent):
            logging.info("Found the concurrent map iteration error in syslog...")
            display.set('status', 'Error detected! Restarting...')
            agent.run("sudo systemctl restart bettercap pwngrid-peer && touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi")
            self.error_counts["concurrent_map"] += 1
            self.ticker += 1

        # Search for the second error message
        search_string_runtime = "panic: runtime error"
        log_file_runtime = "/var/log/syslog"
        if self.search_string_in_log(search_string_runtime, log_file_runtime):
            logging.info("Found the runtime error in syslog...")
            display.set('status', 'Error detected! Restarting...')
            agent.run("sudo systemctl restart bettercap pwngrid-peer && touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi")
            self.error_counts["runtime"] += 1
            self.ticker += 1

        # Restart the device if the set ticker limit is reached. Also reset the variables to avoid weird bugs.
        if self.ticker >= self.ticker_limit:
            self.ticker = 0
            self.error_counts = {
                "concurrent_map": 0,
                "runtime": 0
            }
            logging.info("Error counts before restarting: concurrent map iteration and map write:" +  self.error_counts["concurrent_map"] + "panic: runtime error:" + self.error_counts["runtime"])
            self.restart_device()
