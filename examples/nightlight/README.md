# Nightlight example

A simple little example of how to make a nightlight with the LTR-559 and 5x5 
RGB matrix breakouts. It can be toggled on or off by tapping the sensor, or 
triggered automatically when it gets dark.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat-i2c-spi)
- A Pimoroni [LTR-559 Light & Proximity Sensor Breakout](https://shop.pimoroni.com/products/ltr-559-light-proximity-sensor-breakout)
- A Pimoroni [5x5 RGB Matrix Breakout](https://shop.pimoroni.com/products/5x5-rgb-matrix-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install all of the required libraries.

## Running this example

To run this example, type `./nightlight.py` in the terminal.

You can change the RGB values of the `colour` variable to change the colour 
of the light to whatever you wish. If you want the light and proximity 
thresholds to be more or less sensitive, then you can change the values of 
the `light_threshold` and `prox_threshold` variables.

## Notes

It's probably best to have the sensor and matrix breakouts on either side 
of your Breakout Garden HAT, so that they're spaced apart and the LTR-559 
won't be affected by the light from the matrix.
