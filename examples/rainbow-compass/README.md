# Rainbow compass example

calculates and displays compass heading as an
RGB colour around the hue wheel, with North being red, South cyan,
East green, and West purple, appromximately.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat)
- A Pimoroni [LSM303D Motion Sensor Breakout](https://shop.pimoroni.com/products/lsm303d-6dof-motion-sensor-breakout)
- A Pimoroni [5x5 RGB Matrix Breakout](https://shop.pimoroni.com/products/5x5-rgb-matrix-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh` script in the root of this repository with `sudo ./install.sh` to automagically install all of the required libraries.

## Running this example

To run this example, type `./rainbow-compass.py` in the terminal.

Depending on the orientation of you LSM303D breakout, you can change the line that says `Y = 2` in the `raw_heading` function to e.g. `Y = 1` if you have the breakout flat rather than vertical.
