# pwnagotchi-beacon-plugins
Custom plugin repository

Edit your `/etc/pwnagotchi/config.toml` to look like this

```TOML
main.custom_plugin_repos = [
    "https://github.com/arturandre/pwnagotchi-beacon-plugins/archive/master.zip",
    ]
```
Then run this command: `sudo pwnagotchi plugins update`

## beconify

The messaging system between pwnagotchi units sometimes simply doesn't work. So this plugins tries to fix that by sending the "beacons" directly via a plugin, rather then using pwngrid-peer.

## hashieclean

This version removes "lonely pcaps", those can't be converted
either to the formats .22000 (EAPOL) or .16800 (PMKID). As
the number of lonely pcaps increase the loading time increases
too. Besides that, the checking for completed handshakes
is done more efficiently, thus reducing even further 
the loading time of the plugin.

It is based on (actually build upon) hashi by junohea.mail@gmail.com (their decription):

Attempt to automatically convert pcaps to a crackable format.
If successful, the files  containing the hashes will be saved 
in the same folder as the handshakes. 
The files are saved in their respective Hashcat format:
    - EAPOL hashes are saved as *.22000
    - PMKID hashes are saved as *.16800
All PCAP files without enough information to create a hash are
    stored in a file that can be read by the webgpsmap plugin.

Why use it?:
    - Automatically convert handshakes to crackable formats! 
        We dont all upload our hashes online ;)
    - Repair PMKID handshakes that hcxpcapngtool misses
    - If running at time of handshake capture, on_handshake can
        be used to improve the chance of the repair succeeding
    - Be a completionist! Not enough packets captured to crack a network?
        This generates an output file for the webgpsmap plugin, use the
        location data to revisit networks you need more packets for!
    
Additional information:
    - Currently requires hcxpcapngtool compiled and installed
    - Attempts to repair PMKID hashes when hcxpcapngtool cant find the SSID
    - hcxpcapngtool sometimes has trouble extracting the SSID, so we 
        use the raw 16800 output and attempt to retrieve the SSID via tcpdump
    - When access_point data is available (on_handshake), we leverage 
        the reported AP name and MAC to complete the hash
    - The repair is very basic and could certainly be improved!
Todo:
    Make it so users dont need hcxpcapngtool (unless it gets added to the base image)
        Phase 1: Extract/construct 22000/16800 hashes through tcpdump commands
        Phase 2: Extract/construct 22000/16800 hashes entirely in python
    Improve the code, a lot

## pwnwatch

Work in progress
