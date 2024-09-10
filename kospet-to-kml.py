#!/usr/bin/env python3

from pprint import pprint
import argparse
import json
import re
import xml.etree.ElementTree as ET

__author__ = "github.com/mmanjos"
__copyright__ = "Copyright 2024, Matthew Manjos"
__license__ = "GPL-3"
__version__ = "0.0.1"
__maintainer__ = "Matthew Manjos"
__email__ = "matt@manjos.com"


def get_start_time(jsondata: str):
    """Return a YYYY-MM-DD HH:MM:SS formatted date string from the startTime field of the watch json"""
    start_time = jsondata["startTime"]
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})-(\d{2})", start_time)
    groups = match.groups()
    start_time = (
        groups[0] + "-" + groups[1] + "-" + groups[2] + " " + groups[3] + ":" + groups[4] + ":" + groups[5]
    )
    return start_time


def get_coordinates(jsondata: str):
    """Return a comma-separated string of all long,lat,alt points found in the watch json"""
    # TODO: The Kospet Tank T3 Ultra records all altitude points as 0
    # Hopefully this will be fixed by the manufacturer in a future firmware release
    ret = ""
    for point in jsondata["jsonGpsParams"]:
        ret += (
            str(point["gpsLongitude"]) + "," + str(point["gpsLatitude"]) + "," + str(point["altitude"]) + "\n"
        )
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="Input KOSPET json filename")
    parser.add_argument("-o", "--output", required=True, help="Ouptut KML filename")
    parser.add_argument("-n", "--name", required=False, help="Trip Name (Optional)")
    args = parser.parse_args()

    with open(args.input, "r") as file:
        jsondata = json.load(file)
        jsondata = jsondata["value"][0]

    start_time = get_start_time(jsondata)

    # Start the document
    kml = ET.Element("kml", xmlns="http://www.opengis.net/kml/2.2")
    document = ET.SubElement(kml, "Document")
    placemark = ET.SubElement(document, "Placemark")

    # Include a name tag if specified as an argument
    if args.name:
        name = ET.SubElement(placemark, "name")
        name.text = args.name

    # Set the description of the track to the KOSPET watch string and the start time
    description = ET.SubElement(placemark, "description")
    description.text = "Recorded by KOSPET Watch at " + start_time

    line_string = ET.SubElement(placemark, "LineString")
    coordinates = ET.SubElement(line_string, "coordinates")
    # Fetch the coordinates from the json payload and write store them in the tag
    coordinates.text = get_coordinates(jsondata)

    # Finally, write out the file
    tree = ET.ElementTree(kml)

    print(
        args.output
        + ": writing "
        + str(len(ET.tostring(tree.getroot())))
        + " bytes containing "
        + str(coordinates.text.count("\n"))
        + " GPS points"
    )
    tree.write(args.output)
