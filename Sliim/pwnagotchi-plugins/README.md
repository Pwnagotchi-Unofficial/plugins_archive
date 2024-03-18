# Custom pwnagotchi plugins

These plugins have been tested in pwnagotchi v1.5.5

- [darkmode](#darkmode)
- [gps_error](#gps_error)
- [gps_fix](#gps_fix)
- [gps_grid](#gps_grid)
- [gps_live](#gps_live)
- [gps_sat](#gps_sat)
- [rtc_grid](#rtc_grid)
- [tracker](#tracker)
- [ups_lite_1_2](#ups_lite_1_2)
- [ups_lite_1_3](#ups_lite_1_3)
- [waveshare_v3_touch](#waveshare_v3_touch)
- [xp](#xp)
- [xp_grid](#xp_grid)

![demo](/pwnagotchi1.jpg)

## darkmode

Plugin to enable/disable darkmode by modifying `pwnagotchi.ui.view` constants and update current ui elements.

### Configuration

```
main.plugins.darkmode.enabled = true
```

## gps_error

Plugin to display GPS errors in case the default `gps` plugin:
- is not loaded
- is not running
- receive no data
- is not fixed (FixQuality=0)

Errors are displayed in the default `latitude` ui element.

This plugin requires the default `gps` plugin enabled.

### Configuration

```
main.plugins.gps_error.enabled = true
```

## gps_fix

Plugin to diplay current GPS fix quality.

This plugin requires the default `gps` plugin enabled.

### Configuration

```
main.plugins.gps_fix.enabled = true
main.plugins.gps_fix.position = "0,83"
```

## gps_grid

Plugin to share current GPS data to other units with grid. 
Maybe you don't want to enable this as it send current position in advertissement packets!

This plugin requires the default `gps` plugin enabled.

### Configuration

```
main.plugins.gps_grid.enabled = true
```

## gps_live

Plugin to update GPS coordinates on each epoch.

This plugin requires the default `gps` plugin enabled.

### Configuration

```
main.plugins.gps_live.enabled = true
```

## gps_sat

Plugin to display current number of sattelites.

This plugin requires the default `gps` plugin enabled.

### Configuration

```
main.plugins.gps_sat.enabled = true
main.plugins.gps_sat.position = "90,83"
```

## rtc_grid

Plugin to share timestamp from RTC module with peers.

For units with RTC module: a clock will be displayed and the current timestamp will be shared with grid.
For units without RTC module: they will see if some peers (good friends) share their timestamp and set time from it.

### Configuration

```
main.plugins.rtc_grid.enabled = true
main.plugins.rtc_grid.position = "100,-1"
main.plugins.rtc_grid.peer_position = "242,94"
```

## tracker

Plugin to track every APs and clients seen.

### Configuration

```
main.plugins.tracker.enabled = true
```

This plugin create many files depending of your environment, files are located in `/var/local/pwnagotchi/tracker` directory. It can be useful to mount this directory in memory with this configuration:

```
fs.memory.mounts.data.enabled = true
fs.memory.mounts.data.mount = "/var/local"
fs.memory.mounts.data.size = "50M"
fs.memory.mounts.data.sync = 60
fs.memory.mounts.data.zram = true
fs.memory.mounts.data.rsync = true
```

See https://pwnagotchi.ai/configuration/#sdcard-protection

## ups_lite_1_2

This is a copy of the default `ups_lite` plugins with some additions:
- Don't shutdown if battery is charging

### Configuration

```
main.plugins.ups_lite_1_2.enabled = true
main.plugins.ups_lite_1_2.shutdown = 5
```

## ups_lite_1_3

This is a copy of the default `ups_lite` plugins with some additions:
- Support UPSLite v1.3
- Don't shutdown if battery is charging

### Configuration

```
main.plugins.ups_lite_1_3.enabled = true
main.plugins.ups_lite_1_3.shutdown = 5
```

## waveshare_v3_touch

Experimental plugin to play with Waveshare v3 touch screen. 
This plugin is not currently working..

### Configuration

```
main.plugins.waveshare_v3_touch.enabled = false
```

## xp

Plugin implementing xp/level/ranks for your unit.

- New rank every 5 levels
- Custom heads for each rank
- Provide web ui to follow progression

### Configuration

```
main.plugins.xp.enabled = true
main.plugins.xp.load_initial_xp = false
main.plugins.xp.level_position = "10,30"
main.plugins.xp.rank_position = "50,30"
main.plugins.xp.progressbar_position = "20,40,103,44"
```

## xp_grid

Plugin to share `xp` plugin data (level, rank) with peers.

### Configuration

```
main.plugins.xp_grid.enabled = true
main.plugins.xp_grid.position = "36,95"
main.plugins.xp_grid.name_position = "63,95"
```

This plugin requires the `xp` plugin enabled.
