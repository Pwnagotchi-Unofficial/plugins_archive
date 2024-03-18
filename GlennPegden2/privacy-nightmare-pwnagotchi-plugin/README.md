# privacy-nightmare-pwnagotchi-plugin
A pwnagotchi plugin to supply data to the privacy-nightmare back end

Privacy Nightmare is a project to demostrate just how much innocent metadata is floating around in the air (wifi, cellular, bluetooth, etc) and visible the the naked eye and how this can all be legally assimilated "for evil".

Pwnagotchi is a project by EvilSocket to use a Raspberry Pi Zero to capture PMKIDs from wifi handshakes, but it's also a great framework for a low cost, low power, low form factor generally sniffer.

This modules can be loaded into the pwnagothi just like any other module and collects data to send to PrivacyNightmare.

Currently the data is just collected locally (as the backend isn't ready yet).

Features so far
- Leans on the great AP data collected by the pwnagotchi (far more than is normally shown) including vendor info, wps data etc.
- Also leans on the pwnagotchi gps module to get the gps location of any find

Coming soon
- wifi client info (stuff the pwnagotchi doesn't normally care about)
- wifi home network probes (essentially the work in the https://github.com/GlennPegden2/probe-stalker project)

