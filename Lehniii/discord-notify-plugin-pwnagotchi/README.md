# discord-notify-plugin-pwnagotchi
Unofficial plugin for pwnagotchi -- Send notifications to a Discordchannel via a Webhook when a handshake is captured

## How to install and configure:

### 1. Copy the discord_notify.py into your customplugins folder
### 2. Add following lines in your config.toml, set the discord_notify.webhook to your Disocrd Webhook Url and the discord_notify.name to whatever name you want the Bot to have in your Discord
```
main.plugins.discord_notify.enabled = true
main.plugins.discord_notify.webhook = "Webhookurl"
main.plugins.discord_notify.name = "pwnagotchi"
```
### 3. Restart the pwnagotchi service or reboot the Pi


### And that's it, now you should get a Discord message to your Channel when a handshake is captured. 
Important!! your pwnagotchi needs Internet connection for this so activate Bluetooth Tethering. 
