#!/usr/bin/env python3

import os
import time
import sys

try:
    from PIL import Image
    from PIL import ImageFont
    from PIL import ImageDraw
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

from lsm303d import LSM303D
from threading import Thread
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import sh1106

print("""This Pimoroni Breakout Garden example requires an
LSM303D 6DoF Breakout and a 1.12" OLED Breakout (SPI).

The Dino-Detect v1.2 beta is a dino stomp detector. It's a
UNIX system, I know this.

Press Ctrl+C to exit.
""")

# Set up OLED

oled = sh1106(spi(port=0, device=1, gpio_DC=9), rotate=2, height=128, width=128)

# Load fonts

rr_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf'))
print(rr_path)
rb_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Black.ttf'))
rr_24 = ImageFont.truetype(rr_path, 24)
rb_20 = ImageFont.truetype(rb_path, 20)
rr_12 = ImageFont.truetype(rr_path, 12)

# Set up LSM303D motion sensor

lsm = LSM303D(0x1d)

samples = []
points = []

sx, sy, sz = lsm.accelerometer() # Starting values to zero out accelerometer

sensitivity = 5 # Value from 1 to 10. Determines twitchiness of needle

# Function to thread accelerometer values separately to OLED drawing

def sample():
    while True:
        x, y, z = lsm.accelerometer()

        x -= sx
        y -= sy
        z -= sz

        v = y # Change this axis depending on orientation of breakout

        # Scale up or down depending on sensitivity required

        if v < 0:
            v *= (100 * sensitivity)
        else:
            v *= (40 * sensitivity)


        # Only keep 96 most recent values in list

        points.append(v)
        if len(points) > 96:
            points.pop(0)

        time.sleep(0.05)

# The thread to measure acclerometer values

t = Thread(target=sample)
t.daemon = True
t.start()

# Wait for at least one data oint

while len(points) == 0:
    pass

# The main loop that draws values to the OLED

while True:
    background = Image.open("images/seismograph.png").convert(oled.mode)
    draw = ImageDraw.ImageDraw(background)

    draw.line([(128, 64), (96, 64 + points[-1])], fill="white")
    draw.line([(128, 63), (96, 64 + points[-1])], fill="white")
    draw.line([(128, 65), (96, 64 + points[-1])], fill="white")

    # Draw the seismograph trace

    for i in range(1, len(points)):
        draw.line([(i - 1, 64 + points[i - 1]), (i, 64 + points[i])], fill="white")

    # Draw the Dino-Detect "branding"

    draw.rectangle([(0, 0), (128, 20)], fill="black")
    draw.text((0, 1), "AUS (A UNIX System)", fill="white", font=rr_12)
    draw.line([(0, 20), (128, 20)], fill="white")

    draw.rectangle([(0, 108), (128, 128)], fill="black")
    draw.text((0, 110), "Dino-Detect v1.2 BETA", fill="white", font=rr_12)
    draw.line([(0, 108), (128, 108)], fill="white")

    # Display on the OLED

    oled.display(background)
