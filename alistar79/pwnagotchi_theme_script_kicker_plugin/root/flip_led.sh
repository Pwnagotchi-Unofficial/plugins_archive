#!/bin/bash
if [ `grep -c 'o ooo o o    ooo ooo ooo    o ooo    ooo o o    o    ooo o o    ' /etc/pwnagotchi/config.toml` -eq 1 ];
then
	led_snip="/etc/pwnagotchi/original_led.snip"
else
	led_snip="/etc/pwnagotchi/morse_led.snip"
fi

lead='main.plugins.led.patterns.loaded = "'
tail='main.plugins.led.patterns.peer_lost = "'
sed -i "/$lead/,/$tail/{ /$lead/{r $led_snip
        }; /$tail/d; d }"  /etc/pwnagotchi/config.toml

if [ `/bin/ps afx | grep -v grep| grep -c '/usr/local/bin/pwnagotchi --manual'` -eq 0 ];
then
	touch /root/.pwnagotchi-auto
else
	touch /root/.pwnagotchi-manual
fi

/usr/sbin/service pwnagotchi restart
