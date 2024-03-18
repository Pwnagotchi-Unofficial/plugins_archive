# Pwnagotchi-Handshaker

Plugin to assist with automating tasks and providing access to critical pwnagotchi data when ssh is not available.

**Why?**

Things break, I break things. My RNDIS network device on my Mac disappeared and I have not figured out how to get it back yet but still needed to access data from my pwnagotchi when I was done with a drive and this plugin provided a workable solution and I wanted to share it with others.

**What does it do?**

Currently there are three primary functions that this plugin handles:

- Startup Functions:
  - The /root/handshakes/* directory will be synced with /boot/handshakes/ giving you access to grab any handshake files by inserting the pwnagotchi SD card into a computer.
  - The most recent config.toml file will be copied to /boot/ in order to make changes to it based on its current state
  - The pwnagotchi.log file will be copied to /boot/ so that it can be quickly grabbed for review
- Optional Functions
  - *(In Process, need to finish creating the user options file)* Having issues getting custom plugins up and running or need to do it without ssh access? Create a new folder in /boot/ called 'custom_plugins', drop in your plugin.py files and if Handshaker is running, at startup the folder will be scooped up and any py files will automatically be moved to your designated plugins folder.

Adding more functionality as requested, currently this was to solve a personal issue but thought it could be userful for someone else as well.
