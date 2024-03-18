#!/usr/bin/python3

"""
    problem:
        raspi has no battery buffered clock. on boot its set time to last-file-change of "/var/lib/systemd/timesync/clock"
        the cron makes every minute a "touch /var/lib/systemd/timesync/clock"
        so: raspi always starts with time from last shutdown and syncs time, if internet is available (or gps/* time sync)
    solution:
        we store on every boot the timestamp+uptime. if timestamp/uptime is different over 60s from saved boot values, we know: time was synced
        now we can fix times from before sync time by calculating an offset
    things are possible:
        - store (on saved handshakes 4example) timestamp if synced or if not synced: {"ts": 1571775435, "boot_uuid": "a1f0....e3d", "uptime": 1234}
        - sync time from other already synced pwnagotchi
        - 
"""

import os
from RaspiSyncedTime import RaspiSyncedTime

testdata_dir = os.path.dirname(os.path.realpath(__file__))+"/test_var_pwnagotchi_timesync/"


raspi_synced_time = RaspiSyncedTime( testdata_dir )

print("-test 1)")
print("get time now:")
print(raspi_synced_time.getTime())
print("for test edit ",raspi_synced_time._boot_timesync_json_path,raspi_synced_time._boot_uuid,".json and change 'synced:1' to 0")


print("\n\n-test 2)")
print("get older time from previews boot calculated with offset:")
#aabbccddeeff00112233445566778899.json
old_time={'ts': 1572794250, 'boot_uuid': 'aabbccddeeff00112233445566778899', 'uptime': 11822}
print(raspi_synced_time.getTime(old_time))





