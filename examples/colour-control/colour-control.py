#!/usr/bin/env python3

import time
import colorsys
import atexit

from trackball import TrackBall
from rgbmatrix5x5 import RGBMatrix5x5

print("""This Pimoroni Breakout Garden example requires an
Trackball Breakout and a 5x5 RGB Matrix Breakout.

Use the trackball and switch to control the hue and
brightness of the trackball's RGBW LEDs.

Scroll up to increase brightness and left/right
to change hue. Click to turn on/off.

Press Ctrl+C to exit.
""")

# Set up the trackball
trackball = TrackBall(interrupt_pin=4)

@atexit.register
def clear_trackball():
    trackball.set_rgbw(0, 0, 0, 0)

# Set up the 5x5 RGB matrix
rgbmatrix5x5 = RGBMatrix5x5()
rgbmatrix5x5.set_clear_on_exit()
rgbmatrix5x5.set_brightness(0.8)

x = 0
y = 50.0

toggled = False

while True:
    up, down, left, right, switch, state = trackball.read()

    # Update x and y vals based on movement
    y += up
    y -= down
    x += right / 10.0
    x -= left / 10.0

    # Clamp to min of 0 and max of 100
    x %= 100
    y = max(0, min(y, 100))

    # Calculate hue and brightness
    h = x / 100.0
    v = y / 100.0

    # Prevents button from retriggering
    debounce = 0.5

    # Change toggled state if switch is pressed
    if state and not toggled:
        toggled = True
        time.sleep(debounce)
    elif state and toggled:
        toggled = False
        time.sleep(debounce)

    # Set brightness to zero if switch toggled
    if toggled:
        v = 0

    # Calculate RGB vals
    w = 0
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, v)]

    # Set LEDs
    trackball.set_rgbw(r, g, b, w)
    rgbmatrix5x5.set_all(r, g, b)
    rgbmatrix5x5.show()

    time.sleep(0.01)
