# Pwnagotchi_gpsd-upgraded_plugin

THIS IS A MODIFIED VERSION OF THE KELLERTK GPSD PLUGIN GO CHECK HIS WORK

https://github.com/kellertk/pwnagotchi-plugin-gpsd

# Why ?
I recently asked myself if there was a gps plugin that records gps coordinates and saves the last position so that if, for example, you go into a basement and lose the gps connection it will still records the handshakes with the last recorded position.

The plugin gps_more by Sniffleupagus does something similar but not exactly so I decided to create it myself by modifying the kellertk gpsd plugin. (note that I'm not good in programming and that this is my first project. I asked a friend of mine to help me but there may be better ways of doing what I want.)

I have created two versions of this plugin:

# V1
This is the first version and it stores the last valid gps coordinates on a variable inside the plugin itself, and each time it captures a handshake, it takes the gps coordinates from this variable instead of the gps itself. This can be useful if you enter a building or something and lose the gps connection, the gps doesn't send data anymore but it will take the last position saved in the variable and record your handshakes with it.

# V2
The V2 goes a bit further and becareful because it may not be suitable for all users depending on their usage. This version does the same thing as the V1, but saves the last valid gps coordinates into an external file and loads them each time the pwnagotchi boot up. In the first plugin, when the pwnagotchi is restarted, it loses the last valid gps coordinates saved. In my use where every time I move my pwnagotchi it's turned on, every time it starts up it took a few minutes to capture gps data, which annoyed me because I inevitably lost gps data on the first few handshakes I captured. Now it has gps data as soon as it starts up.

!!!!! This can introduce false gps data if it is started at a location other than where it was switched off !!!!! 

# Requirements

You'll need a configured <code>gpsd</code>, and also <code>gpsd-py3</code>.

To do that I invite you to go to the Kellertk gpsd plugin page and see the his requirements section.

https://github.com/kellertk/pwnagotchi-plugin-gpsd

# Setup
Put the gpsd.py file into your installed plugins directory and add this to your <code>config.toml</code> file. The filelocation line is the location where the gps coordinate will be saved on the V2 version so if you install the V1 it's not necessary to add it !

<pre>
main.plugins.gpsd.enabled = true
main.plugins.gpsd.gpsdhost = "127.0.0.1"
main.plugins.gpsd.gpsdport = 2947
main.plugins.gpsd.filelocation = "/usr/local/share/pwnagotchi/installed-plugins/lastsessiongps.json" #only useful on the V2
</pre>
