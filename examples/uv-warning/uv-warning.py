#!/usr/bin/env python3

import os
import sys
import time
import veml6075
import smbus
import colorsys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106
from rgbmatrix5x5 import RGBMatrix5x5

print("""
This Pimoroni Breakout Garden example requires a VEML6075 UV
Breakout, a 5x5 RGB Matrix Breakout, and a 1.12" OLED Breakout.

The UV-O-Meter 3000 displays UV levels visually and in text.

Press Ctrl+C a couple times to exit.
""")

# Map UV index to a descriptive level

def uv_to_description(avg_uv_index):
    if avg_uv_index < 3:
        return "LOW"
    elif 3 <= avg_uv_index < 6:
        return "MEDIUM"
    elif 6 <= avg_uv_index < 8:
        return "HIGH"
    elif 8 <= avg_uv_index < 11:
        return "V. HIGH"
    elif avg_uv_index > 11:
        return "EXTREME"
    else:
        return ""

bus = smbus.SMBus(1)

# Set up UV sensor
uv_sensor = veml6075.VEML6075(i2c_dev=bus)
uv_sensor.set_shutdown(False)
uv_sensor.set_high_dynamic_range(False)
uv_sensor.set_integration_time('100ms')

# Set up RGB matrix
rgbmatrix5x5 = RGBMatrix5x5()
rgbmatrix5x5.set_clear_on_exit()
rgbmatrix5x5.set_brightness(1.0)

# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)

# Load fonts
rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Black.ttf'))
rb_15 = ImageFont.truetype(rb_path, 15)
rr_15 = ImageFont.truetype(rr_path, 15)

while True:
    try:
        img = Image.open("images/uv-warning.png").convert(oled.mode)
        draw = ImageDraw.Draw(img)

        draw.rectangle([(0, 0), (128, 128)], fill="black")

        # Get UV data and calculate indices
        uva, uvb = uv_sensor.get_measurements()
        uv_comp1, uv_comp2 = uv_sensor.get_comparitor_readings()
        uv_indices = uv_sensor.convert_to_index(uva, uvb, uv_comp1, uv_comp2)
        uva_index, uvb_index, avg_uv_index = uv_indices

        # Draw UV data to OLED
        draw.text((0, 0), "UV-O-Meter 3000", fill="white", font=rb_15)
        draw.text((0, 30), "UVA index:  {:05.02f}".format(uva_index), fill="white", font=rr_15)
        draw.text((0, 48), "UVB index:  {:05.02f}".format(uvb_index), fill="white", font=rr_15)
        draw.text((0, 66), "Avg. index:  {:05.02f}".format(avg_uv_index), fill="white", font=rr_15)
        draw.text((0, 100), "Level: {}".format(uv_to_description(avg_uv_index)), fill="white", font=rb_15)

        # Map avg. UV index to colour, from green to red
        hue = (10.001 - min(10, avg_uv_index)) / 30
        sat = 1.0
        val = 1.0
        r, g, b = [int(255 * c) for c in colorsys.hsv_to_rgb(hue, sat, val)]

        # Light RGB matrix with calculated colour
        rgbmatrix5x5.set_all(r, g, b)
        rgbmatrix5x5.show()
        oled.display(img)

        # Also print current UV index
        print ('Avg. UV index: {}'.format(avg_uv_index))

    except KeyboardInterrupt:
        sys.exit(0)
