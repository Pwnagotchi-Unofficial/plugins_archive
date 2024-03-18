# Pwnagotchi-plugins
A small collection of created and modified script and plugins for pwnagotchi 


- quickdic.py : 
A cracking plugins that check for handshake and PMKID when a PCAP is captured. Use small dictonnary or it take a while to finish. Also take care of temperature when cracking on RPI 0w2 only the wordlist is calibred to get 30 second maximum of cracking to ensure a no overheating when multiple pcap is receive.

- wpa-sec.cracked.potfile :
pot file that contain cracked and failed SSID.

- mini-8.txt : 
Custom homemade wordlist to crack simple 8 length password.

- display-password.py : 
Display the last tested PCAP : SSID - FAIL if fail or SSID - password if cracked and the last cracked password SSID - password

- display-aircrack.py : 
Display if aircrack is currently running with (0) off or (1) running

- pwnaget.py : 
Python script to automatically ssh into the pwnagotchi, grab all pcap file in directory mentionned, convert it directly in a hashcat format that can be concatened in one file with *.hccapx > all.hccapx 

---
Warning
---
Remember to use in ethical way. 

- file needed : /home/pi/mini-8.txt
- and :  /home/pi/wpa-sec.cracked.potfile 


- Activation of plugins : 

main.plugins.display-password.enabled = true
main.plugins.display-aircrack.enabled = true

main.plugins.quickdic.enabled = true
main.plugins.quickdic.face = "(·ω·)"

main.plugins.aircrackonly.enabled = true
main.plugins.aircrackonly.face = "(>.<)"
