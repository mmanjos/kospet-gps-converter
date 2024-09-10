# kospet-gps-converter

## Introduction

This tool was written to convert the proprietary JSON route recording from KOSPET GPS-enabled Smart Watches into a standard KML file that can then be used with apps like [Wanderer](https://github.com/Flomp/wanderer).

## Compatability

So far, this project has only been tested against these watches. Please report if you were able to get it working on another watch or firmware combo!

| Watch                                                                               | Firmware      | Supported                                |
| ----------------------------------------------------------------------------------- | ------------- | ---------------------------------------- |
| [KOSPET Tank T3 Ultra](https://kospet.com/products/kospet-tank-t3-ultra-smartwatch) | AT341DV001134 | :white_check_mark: Lat/Long :x: Altitude |

:warning: The current firmware on the Tank T3 Ultra unfortunately records `altitude: 0` at all points in the data. A request has been made to the manufacturer to have this valuable data saved in future releases.

## Usage

### Part One: Retrieve the JSON File

_Note: you will need to have your Android phone rooted for this to work_

GPS Route data that has been recorded by the watch gets written to JSON files on your phone after the watch syncs to the [KOSPET Fit](https://play.google.com/store/apps/details?id=com.yc.kospetfit) app.

These files get written to this path on the Android phone: `/data/media/0/Android/data/com.yc.kospetfit/files/upload/sport/json/`

Fetch all of the GPS routes with these commands:

```
adb shell su -c tar cvf /sdcard/Download/kospet-gps-json.tar /data/media/0/Android/data/com.yc.kospetfit/files/upload/sport/json/*.json
adb pull /sdcard/Download/kospet-gps-json.tar
adb shell rm /sdcard/Download/kospet-gps-json.tar
tar xvf kospet-gps-json.tar
```

### Part Two: Converting JSON Files

```
usage: kospet-to-kml.py [-h] -i INPUT -o OUTPUT [-n NAME]
```

For example, to convert the route `20240830.json` off of the watch into `grand-canyon-hike.kml` you can use the following command:

```
python kospet-to-kml.py -i 20240830.json -o grand-canyon-hike.kml -n "Grand Canyon Rim-to-Rim Hike"
```
