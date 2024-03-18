#!/bin/bash
if [ `grep -c 'WHITE = 0xff' /usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/view.py` -eq 1 ];
then
	sed -i 's/WHITE = 0xff/WHITE = 0x00/;s/BLACK = 0x00/BLACK = 0xff/' /usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/view.py
else
	sed -i 's/WHITE = 0x00/WHITE = 0xff/;s/BLACK = 0xff/BLACK = 0x00/' /usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/view.py
fi

if [ `/bin/ps afx | grep -v grep| grep -c '/usr/local/bin/pwnagotchi --manual'` -eq 0 ];
then
	touch /root/.pwnagotchi-auto
else
	touch /root/.pwnagotchi-manual
fi

/usr/sbin/service pwnagotchi restart
