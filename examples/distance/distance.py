#!/usr/bin/env python3

import os
import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

import VL53L1X

from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106

print("""This Pimoroni Breakout Garden example requires an
VL53L1X Time of Flight Sensor Breakout and a 1.12" OLED Breakout (SPI).

The Park-O-Matic 6000 is a car reversing indicator mockup!

Press Ctrl+C a couple times to exit.
""")

# Set up OLED

oled = sh1106(spi(port=0, device=1, gpio_DC=9), rotate=2, height=128, width=128)

# Set up VL53L1X Time of Flight sensor

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open() # Initialise the I2C bus and configure the sensor
tof.start_ranging(3) # Start ranging, 1 = Short Range, 2 = Medium Range, 3 = Long Range


# Load fonts

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
rb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Black.ttf'))
rr_24 = ImageFont.truetype(rr_path, 24)
rb_20 = ImageFont.truetype(rb_path, 20)
rr_12 = ImageFont.truetype(rr_path, 12)


i = 0
threshold = 20 # Threshold at which the warning indicator flashes, in cm

# Main loop

while True:
    i += 1

    background = Image.open("images/distance.png").convert(oled.mode) # Load the artwork

    draw = ImageDraw.ImageDraw(background)

    # Measure the distance and write to the right place on the display

    cm = tof.get_distance() // 10
    cm += 1
    pos = 80 - (rb_20.getsize(str(cm))[0] / 2)
    draw.text((pos, 30), "{}".format(cm), fill="white", font=rb_20)

    # Flash the warning indicator if the distance is below the threshold

    if cm > threshold or i % cm == 1:
        draw.rectangle([(76, 66), (115, 110)], fill="black")

    # Display on the OLED

    oled.display(background)

    time.sleep(0.05)
