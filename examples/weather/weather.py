#!/usr/bin/env python3

import os
import time
import datetime
import json
import urllib
import glob

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import bme680

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

print("""This Pimoroni Breakout Garden example requires a
BME680 Environmental Sensor Breakout and a 1.12" OLED Breakout.

This example turns your Breakout Garden into a mini weather display
combining indoor temperature and pressure data with a weather icon
indicating the current local weather conditions.

Press Ctrl+C a couple times to exit.
""")

# Default to Sheffield-on-Sea for location

CITY = "Sheffield"
COUNTRYCODE = "GB"

# Uses IP address to determine location. If you don't want to do this, then
# remove the get_location() call below and hard-code values above.

def get_location():
    res = requests.get('http://ipinfo.io')
    if(res.status_code == 200):
        json_data = json.loads(res.text)
        return json_data
    return {}

# URL-encoding function for weather API call

def encode(qs):
    val = ""
    try:
        val = urllib.urlencode(qs).replace("+","%20")
    except:
        val = urllib.parse.urlencode(qs).replace("+", "%20")
    return val

# Finds the weather code by querying the Yahoo weather API for your location.
# The weather code is used to display the weather icon.

def get_weather_code(address):
    base = "https://query.yahooapis.com/v1/public/yql?"
    query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\""+address+"\")"
    qs={"q": query, "format": "json", "env": "store://datatables.org/alltableswithkeys"}

    uri = base + encode(qs)
    res = requests.get(uri)

    if(res.status_code==200):
        json_data = json.loads(res.text)
        if "channel" in json_data["query"]["results"]:
            results = json_data["query"]["results"]["channel"]
            code = int(results["item"]["forecast"][0]["code"])
            return code

    return {}

# icon_map maps Yahoo weather API codes to weather names, to make selection
# of the weather icons easy

icon_map = {
    "snow": [5, 6, 7, 8, 10, 13, 14, 15, 16, 17, 18, 41, 42, 43, 46],
    "rain": [9, 11, 12],
    "cloudy": [19, 20, 21, 22, 25, 26, 27, 28, 29, 30, 44],
    "sun": [32, 36],
    "fair": [33, 34],
    "storm": [0, 1, 2, 3, 4, 37, 38, 39, 45, 47],
    "wind": [23, 24]
}

# Pre-load icons into a dictionary with PIL

icons = {}

for icon in glob.glob("icons/*.png"):
    icon_name = icon.split("/")[1].replace(".png", "")
    icon_image = Image.open(icon)
    icons[icon_name] = icon_image

weather_icon = None

# Determines location based on IP address. Comment out the lines
# below if you don't want to do this, and hard-code the CITY and
# COUNTRYCODE variables at the top.

###############################################################
# Remove or comment out these line to disable IP address lookup
# and change the CITY and COUNTRYCODE variables above to your
# current city and country.
###############################################################

try:
    loc_data = get_location()
    CITY = loc_data["city"]
    COUNTRYCODE = loc_data["country"]
except:
    pass

###############################################################

location_string = "{city}, {countrycode}".format(city=CITY, countrycode=COUNTRYCODE)

# Set up OLED

oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)

# Set up BME680 sensor

sensor = bme680.BME680()

sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

# Load fonts

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Black.ttf'))
rr_24 = ImageFont.truetype(rr_path, 24)
rb_20 = ImageFont.truetype(rb_path, 20)
rr_12 = ImageFont.truetype(rr_path, 12)

# Initial values

low_temp = sensor.data.temperature
high_temp = sensor.data.temperature
curr_date = datetime.date.today().day

code = get_weather_code(location_string)
last_checked = time.time()

weather_icon = None

# Main loop

while True:
    if time.time() - last_checked > 60: # Limit calls to Yahoo weather API to 1 per minute
        code = get_weather_code(location_string)
        last_checked = time.time()
    for icon in icon_map: # Find correct weather icon for code
        if code in icon_map[icon]:
            weather_icon = icons[icon]
            break

    # Load in the background image

    background = Image.open("images/weather.png").convert(oled.mode)

    # Place the weather icon and draw the background

    background.paste(weather_icon, (10, 46))
    draw = ImageDraw.ImageDraw(background)

    # Gets temp. and press. and keeps track of daily min and max temp.

    if sensor.get_sensor_data():
        temp = sensor.data.temperature
        press = sensor.data.pressure
        if datetime.datetime.today().day == curr_date:
            if temp < low_temp:
                low_temp = temp
            elif temp > high_temp:
                high_temp = temp
        else:
            curr_date = datetime.datetime.today().day
            low_temp = temp
            high_temp = temp

        # Write temp. and press. to image

        draw.text((8, 22), "{0: >4}".format(int(press)), fill="white", font=rb_20)
        draw.text((86, 12), "{0: >2}°".format(int(temp)), fill="white", font=rb_20)

        # Write min and max temp. to image

        draw.text((80, 0), "max: {0: >2}°".format(int(high_temp)), fill="white", font=rr_12)
        draw.text((80, 110), "min: {0: >2}°".format(int(low_temp)), fill="white", font=rr_12)

    # Write the 24h time and blink the separator every second

    if int(time.time()) % 2 == 0:
        draw.text((4, 98), datetime.datetime.now().strftime("%H:%M"), fill="white", font=rr_24)
    else:
        draw.text((4, 98), datetime.datetime.now().strftime("%H %M"), fill="white", font=rr_24)

    # These lines display the temp. on the thermometer image

    draw.rectangle([(97, 43), (100, 86)], fill="black")
    temp_offset = 86 - ((86 - 43) * ((temp - 20) / (32 - 20)))
    print(temp_offset)
    draw.rectangle([(97, temp_offset), (100, 86)], fill="white")

    oled.display(background) # Display the completed image on the OLED

    time.sleep(0.1)

