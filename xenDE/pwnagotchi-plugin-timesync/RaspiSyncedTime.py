__author__ = 'https://github.com/xenDE/pwnagotchi-plugin-timesync'
__version__ = '1.0.0-alpha'
__name__ = 'timesync'
__license__ = 'GPL3'
__description__ = 'calculates an offset after the time of the rasperry pi has been syncronized and can then correct times before the time of the syncronization'

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

#2do: replace print by logging.debug

import logging
import os
import json
import hashlib
import time


class RaspiSyncedTime:
    """
    Class for synced timestamps
    """

    # getTime() returns NOW:
    #   int(1571775435)     timestamp, if time is synced
    #   dict({"ts": 1571775435, "boot_uuid": "a1f0....e3d", "uptime": 1234})      if not synced

    # request a synced timestamp:
    # getTime( {"ts": 1571775435, "boot_uuid": "a1f0....e3d", "uptime": 1234} )
    # returns:
    #   int(1571775435)     timestamp, if time are synced
    #   dict({"ts": 1571775435, "boot_uuid": "a1f0....e3d", "uptime": 1234})      if not synced


    cached_boot_times = {}

    _boot_uuid = ""
    _is_synced = 0

    _check_sync_last_utime = 0
    _check_sync_interval = 60   # check all 60 seconds for synced time
    _boot_timesync_json_path = "/var/pwnagotchi/timesync/"  # needs to end with /

    def __init__(self, boot_timesync_json_path = None):
        if boot_timesync_json_path is not None:
            self._boot_timesync_json_path = boot_timesync_json_path
        try:
            with open("/var/lib/systemd/random-seed", "rb") as f:
                random_seed_data = f.read()
            f.close()
            self._boot_uuid = hashlib.md5(random_seed_data).hexdigest();
        except Exception as error:
            print("error on reading /var/lib/systemd/random-seed: ", error)
        self.cached_boot_times[self._boot_uuid] = self._getJsonBootDict(self._boot_uuid)
        self._is_synced = self.cached_boot_times[self._boot_uuid]["synced"]
        if self._is_synced == 0:
            self._checkSync()
        # make second check for already synced ad boot time before boot

    def getTime(self, intime = None):
        if isinstance(intime, int):
            return intime   # is timestamp
        elif intime is None:
            if self._is_synced != 1:
                print("my boot time is not synced")
                self._checkSync()   # try to calc offset for this boot
            if self._is_synced == 1:
                print("time(NOW) is already synced")
                return int("%.0f" % time.time())
            else:
                print("time(NOW) is NOT synced")
                return {"ts": int("%.0f" % time.time()), "boot_uuid": self._boot_uuid, "uptime": self._getUptime()}
        elif isinstance(intime, dict):
            print("try to sync given timeDict")
            return self.getSynced(intime)
        else:
            logging.error("unknown time format")

    def _getJsonBootDict(self, boot_uuid):
        if boot_uuid != self._boot_uuid:
            if boot_uuid in self.cached_boot_times:
                return self.cached_boot_times[boot_uuid]    # if other boot and already in cache
        if boot_uuid == self._boot_uuid:
            if boot_uuid in self.cached_boot_times:
                if self.cached_boot_times[boot_uuid]["synced"] == 1:
                    return self.cached_boot_times[boot_uuid]    # already synced
        file_name = self._boot_timesync_json_path + boot_uuid + ".json"
        try:
            with open(file_name, 'r') as json_file:
                self.cached_boot_times[boot_uuid] = json.load(json_file)
                return self.cached_boot_times[boot_uuid]
        except json.JSONDecodeError as js_e:
            return None # boot_uuid does not exist or is not readable json

    def _getUptime(self):
        with open("/proc/uptime","r") as f:
            uptime = f.read()
        f.close()
        return int("%.0f" % float(uptime.split(' ')[0]))

    def getSynced(self, timeDict):
        if isinstance(timeDict, int):
            return timeDict   # is timestamp, should be correct
        self._checkSync()   # try to calc offset for this boot
        check_boot = self._getJsonBootDict(timeDict["boot_uuid"])
        if check_boot is None:
            return timeDict # no boot_uuid data - can not proccess
        if check_boot["synced"] == 0:
            return timeDict # have no sync for this boot - can not calc offset
        else:   # sync data / offset is available
            if timeDict["uptime"] < check_boot["sync"]["uptime"]:
                # needs sync
                print("sync time with offset ", check_boot["sync"]["offset"])
                cleaned_ts = timeDict["ts"] + check_boot["sync"]["offset"]
                return int(cleaned_ts)
            else:
                # needs to be checked for already synced time
                if check_boot["boot_ts"]-check_boot["boot_uptime"] != timeDict["ts"]-timeDict["uptime"]:
                    return int(timeDict["ts"] + check_boot["sync"]["offset"])

    def _checkSync(self):
        print("_checkSync() called")
        if self._is_synced == 1:
            print("_checkSync() canceled: already in sync")
            return  # already synced
        uptime = self._getUptime()
        if uptime - self._check_sync_last_utime > self._check_sync_interval:
            self._check_sync_last_utime = uptime
        else:
            return  # not over interval
        # calc offset
        boot_time = self._getJsonBootDict(self._boot_uuid)
        boot_offset = boot_time["boot_ts"] - boot_time["boot_uptime"]
        now_ts = int("%.0f" % time.time())
        now_offset = now_ts - uptime
        offset = now_offset - boot_offset
        print("calculated offset is: ", offset)
        if abs(offset) > 10:    # sync diff > 10 seconds
            boot_time["synced"] = 1
            boot_time["sync"]["offset"] = offset
            boot_time["sync"]["uptime"] = uptime
            try:
                file_name = self._boot_timesync_json_path + self._boot_uuid + ".json"
                with open(file_name, 'w+t') as uuid_json_file:
                    json.dump(boot_time, uuid_json_file)
            except OSError as os_e:
                logging.error("TIME-SYNC: %s", os_e)
            print("system time was synced, calculated offset: ", offset)
            self.cached_boot_times[self._boot_uuid] = boot_time
            self._is_synced = 1

