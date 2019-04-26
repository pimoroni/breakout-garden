#!/usr/bin/env python

import time
import math
import colorsys
from lsm303d import LSM303D
from rgbmatrix5x5 import RGBMatrix5x5

print("""This Pimoroni Breakout Garden example requires an LSM303D
Motion Sensor Breakout and a 5x5 RGB Matrix Breakout.

The Rainbow Compass calculates and displays compass heading as an
RGB colour around the hue wheel, with North being red, South cyan,
East green, and West purple, appromximately.

Press Cyrl-+C to exit.
""")


def raw_heading(minimums, maximums, zero=0):
    """Return a raw compass heading calculated from the magnetometer data."""

    X = 0
    Y = 2  # Change to 1 if you have the breakout flat

    # The range over which values will be calculated, i.e. -1 to +1
    mag_range = 2

    # Get the magnetometer's values
    mag = list(lsm.magnetometer())

    # Scale and shift values
    for i in range(len(mag)):
        mag[i] = ((mag_range / (maximums[i] - minimums[i])) * mag[i]) - \
                 (mag_range / 2.0)

    # Calculate the heading from the vector
    heading = math.atan2(mag[Y], mag[X])

    if heading < 0:
        heading += (2 * math.pi)

    # Convert radian value to degrees
    heading_degrees = (round(math.degrees(heading), 2) - zero) % 360

    return heading_degrees


lsm = LSM303D(0x1d)  # Change to 0x1e if you have soldered the address jumper

# Set up the 5x5 RGB matrix
rgbmatrix5x5 = RGBMatrix5x5()
rgbmatrix5x5.set_clear_on_exit()
rgbmatrix5x5.set_brightness(0.8)

# Python 2/3 compatibility
try:
    input = raw_input
except NameError:
    pass

input("Lay your LSM303D in Breakout Garden flat (LSM303D vertical), \n\
press a key to start, then rotate it 360 degrees, keeping it flat...\n")

# Variables to govern calibration time
t_start = time.time()
t_elapsed = 0
calibration_time = 30

# Initial values for mins and maxs
minimums = list(lsm.magnetometer())
maximums = list(lsm.magnetometer())

# Run calibration until time limit is reached
while t_elapsed < calibration_time:
    mag = lsm.magnetometer()
    for i in range(len(mag)):
        if mag[i] < minimums[i]:  # Set new min
            minimums[i] = mag[i]
        if mag[i] > maximums[i]:  # Set new max
            maximums[i] = mag[i]
    t_elapsed = time.time() - t_start

input("Calibration complete!\n\nIf you want to set a zero (North) point, \n\
then turn your breakout to that point and press a key...\n")

# Zero point for the compass
zero = raw_heading(minimums, maximums)

input("Press a key to begin readings!\n")

# Begin compass readings and display on RGB matrix
while True:
    rh = raw_heading(minimums, maximums, zero=zero)
    hue = rh / 360.0  # Hue is based on compass heading
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(hue, 1.0, 1.0)]
    rgbmatrix5x5.set_all(r, g, b)  # Set whole matrix to calculated RGB
    rgbmatrix5x5.show()
    print("compass heading: {:0.0f} degrees".format(rh))
    time.sleep(0.1)
