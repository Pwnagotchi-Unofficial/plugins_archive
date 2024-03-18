#!/bin/bash
if [ `grep -c LOOK-R.png /etc/pwnagotchi/config.toml` -eq 1 ];
then
	face_snip="/etc/pwnagotchi/emoji_face.snip"
else
	face_snip="/etc/pwnagotchi/punk_face.snip"
fi

lead='^ui.faces.look_r = "'
tail='^ui.faces.icon ='
sed -i "/$lead/,/$tail/{ /$lead/{r $face_snip
        }; /$tail/d; d }"  /etc/pwnagotchi/config.toml

if [ `/bin/ps afx | grep -v grep| grep -c '/usr/local/bin/pwnagotchi --manual'` -eq 0 ];
then
	touch /root/.pwnagotchi-auto
else
	touch /root/.pwnagotchi-manual
fi

/usr/sbin/service pwnagotchi restart
