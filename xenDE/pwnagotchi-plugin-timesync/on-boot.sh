#!/bin/bash

# pownagotchi time sync - https://github.com/xenDE/pwnagotchi-plugin-timesync

# run this script in /etc/rc.local

# save uptime and systime in seconds
pts_boot_uuid=$(md5sum /var/lib/systemd/random-seed | awk '{ print $1 }')
pts_boot_uptime=$(printf "%.0f" "$(cat /proc/uptime | awk '{ print $1 }')")
pts_boot_ts=$(date +%s)
pts_boot_synced=0

timedatectl status | grep "System clock synchronized:" | grep -q "yes"
if [ "$?" -eq "0" ];
then
  pts_boot_synced=1
fi

mkdir -p /var/pwnagotchi/timesync
echo -n "{\"boot_uuid\":\"$pts_boot_uuid\",\"boot_uptime\":$pts_boot_uptime,\"boot_ts\":$pts_boot_ts,\"synced\":$pts_boot_synced,\"sync\":{\"offset\":0,\"uptime\":0}}" > /var/pwnagotchi/timesync/$pts_boot_uuid.json

# example: {"boot_uuid":"20c1b2f8e7b35dc27222e77c1bc20806","boot_uptime":3147,"boot_ts":1571495802,"synced":0,sync:{offset:0,uptime:0}}

