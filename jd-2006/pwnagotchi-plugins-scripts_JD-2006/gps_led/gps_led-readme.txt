I don't use a screen so I wanted a way to know I was getting GPS date before warwalking.
I also do not have GPSD installed. Dunno if that matters or not.

Make sure to use at least a 550 ohm resistor on the positive leg of the LED.

Setting up requires getting GPIO's ready.

To get a list of your GPIO's:
$ raspi-gpio get

All of the GPIO pins are listed with their BCM pin numbers and associated attributes. We won’t get into the details of what it all means, but in general, level shows whether a pin is high (1) or low (0) and func shows whether a pin is set as an input or an output for standard GPIO pins.

You can add a pin number to the end of that command to retrieve only the information for that particular pin. For example, entering the following command:
$ raspi-gpio get 26

GPIO 26: level=0 fsel=0 func=INPUT

The pin is currently set as an input with a low level.

We need to configure it as an output in order to “drive” our LED. This is done with the set sub-command of the raspi-gpio utility:
$ raspi-gpio set 26 op

To test we can then turn on our LED with the command:
$ raspi-gpio set 26 dh

and turn off the LED with the following command:
$ raspi-gpio set 26 dl
