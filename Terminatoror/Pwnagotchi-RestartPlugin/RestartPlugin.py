import re
import time
import logging
from pwnagotchi import plugins, config
from pwnagotchi.plugins import Plugin


class RestartPlugin(plugins.Plugin):
    __author__ = 'Discord: terminatoror'
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'This plugin restarts the pwnagotchi in case bettercap crashes. Heavily based on the restart scripts made by Discord: _dal_ '

    def __init__(self):
        super().__init__()

    def on_loaded(self):
        logging.info('RestartPlugin loaded...')
        self.running = True

    @staticmethod
    def search_string_in_log(search_string, log_file):
        try:
            with open(log_file, "r") as f:
                for line in f:
                    if re.search(search_string, line):
                        return True
        except Exception as e:
            logging.error(f"Error while searching log: {e}")
        return False

    @on_event("beacon")
    def search_log_for_errors(self, agent, **kwargs):
        # Search for the first error message
        search_string_concurrent = "fatal error: concurrent map iteration and map write"
        log_file_concurrent = "/var/log/syslog"
        if self.search_string_in_log(search_string_concurrent, log_file_concurrent):
            logging.info("Found the concurrent map iteration error in syslog, executing command...")
            # Insert your command here:
            # For Pwnagotchi-specific operations, you can use `agent` like:
            # agent.run(f"sudo systemctl restart bettercap pwngrid-peer && touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi")
            time.sleep(10)
            logging.info('RestartPlugin: detected error (fatal error: concurrent map iteration and map write) restarting now...')
            display.set('status', 'Error detected! Restarting...')
            agent.run("sudo systemctl restart bettercap pwngrid-peer && touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi")
            # just to add some time puffer in case the error gets found
            time.sleep(45)



        # Search for the second error message
        search_string_runtime = "panic: runtime error"
        log_file_runtime = "/var/log/syslog"
        if self.search_string_in_log(search_string_runtime, log_file_runtime):
            logging.info("Found the runtime error in syslog, executing command...")
            # Insert your command here:
            # For Pwnagotchi-specific operations, you can use `agent` like:
            # agent.run(f"sudo systemctl restart bettercap pwngrid-peer && touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi")
            time.sleep(10)
            logging.info('RestartPlugin: detected error (panic: runtime error) restarting now...')
            display.set('status', 'Error detected! Restarting...')
            agent.run("sudo systemctl restart bettercap pwngrid-peer && touch /root/.pwnagotchi-auto && systemctl restart pwnagotchi")
            # just to add some time puffer in case the error gets found
            time.sleep(45)
