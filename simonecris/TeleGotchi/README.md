# TeleGotchi | Pwnagotchi Telegram plugin
An interactive Telegram plugin to remotly manage your Pwnagotchi and get real time notifications for new captured handshakes. 

Who wants to connect cables and dump data manually, when you can do it on the fly? 🐱‍🏍

The implemented functionalities are intended to speed up the workflow using a Pwnagotchi, allowing the full control of the device from your smartphone/PC (using Telegram). 

## Features
- Notification when a new handshake is captured, with contextual menu and download options:

  ![new_hs](https://github.com/simonecris/TeleGotchi/assets/63792651/63ad59b0-c0fb-4697-8708-c51f47d670b0)
    - **pcap**: Download original caputed .pcap file.
    - **hashcat**: Convert pcap to Hashcat .22000 file, ready to download.
    - **wordlist**: Generate a wordlist based on ESSID, ready to download. 
- Download any captured handshake using 🧰 Toolbox -> 💾️ **Handshakes downloader**.

  ![downloader](https://github.com/simonecris/TeleGotchi/assets/63792651/7f76a3fa-db27-4150-a1b0-fdb999154b3e)
- Inline Keyboard navigation menu, with different device management options. Eg. ⚙️ **Manage device**:

  ![image](https://github.com/simonecris/TeleGotchi/assets/63792651/0ba14091-68d6-45ae-81c5-9eb15f8a03dc)
- Backup important directories/files and download it as a tar.gz file. 

and much more! 

## Installation
1. Install dependencies and necessary tools. 

SSH to your pwnagotchi and run the following commands:
```
sudo pip3 uninstall telegram python-telegram-bot
sudo pip3 install python-telegram-bot=13.15

# hcxtools (required for hashcat and wordlist generation)
apt install -y python3-requests build-essential pkg-config libcurl4-openssl-dev libssl-dev zlib1g-dev make gcc
wget https://github.com/ZerBea/hcxtools/archive/refs/tags/6.2.7.tar.gz
tar xzvf 6.2.7.tar.gz && cd hcxtools-6.2.7
make
make install
```
2. Copy telegram.py file inside the custom plugins folder.

Default path is:
```
/usr/local/share/pwnagotchi/custom-plugins
```

3. Edit the `/etc/pwnagotchi/config.toml` file with the following:

```
main.plugins.telegram.enabled = true
main.plugins.telegram.bot_token = "BOT_TOKEN"
main.plugins.telegram.chat_id = "CHAT_ID"
main.plugins.telegram.rotate_image = false
main.plugins.telegram.bot_name = "TeleGotchi"
main.plugins.telegram.send_message = true
```
Where `BOT_TOKEN` is the token provided by the Bot Father when you create a new bot. 

The `CHAT_ID` is the ID of the chat where the bot will send handshake notifications. The fastest way to obtain it is by using Telegram Web, open the group chat the bot is member of and copy the ID in the URL bar: `https://web.telegram.org/k/#CHAT_ID`. Make sure the bot has the right permissions!

The `rotate_image` is for the 📸 Screenshot function, in case you need to flip the image vertically. 

## Acknowledgment

Big thanks to https://github.com/wpa-2 for the initial plugin idea.

## Disclaimer and notes

This plugin is for educational purposes only. I take no responsibility for its usage by third parties, and any illegal activities are strictly prohibited. Use at your own risk.  
