import pwnagotchi.plugins as plugins
import requests

class discord_notify(plugins.Plugin):
    __author__ = "Lehni"
    __version__ = '1.0.0'
    __license__ = 'GPL3'
    __description__ = 'Send notifications to a Discordchannel via a Webhook'

    def __init__(self):
        self.webhook = "http://127.0.0.1/"
        self.name = "pwnagotchi"

        
    def on_loaded(self):
        self.webhook = self.options['webhook']
        self.name = self.options['name']


    def on_handshake(self, agent, access_point, client_station):
        data = {
            "content" : "New handshake acquired",
            "username" : self.name,
        }
        requests.post(self.webhook, json=data)

