# UV warning example

This example uses a VEML6075 UVA/B sensor, a 5x5 RGB matrix, and a 1.2" OLED breakout
to display average UV index as a traffic light warning on the RGB matrix, with green
being a low UV index, yellow/orange being moderate, and red high or extreme. The numerical
values and a descriptive warning are displayed on the OLED.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat)
- A Pimoroni [VEML6075 UVA/B Sensor Breakout Breakout](https://shop.pimoroni.com/products/veml6075-uva-b-sensor-breakout)
- A Pimoroni [5x5 RGB Matrix Breakout](https://shop.pimoroni.com/products/5x5-rgb-matrix-breakout)
- A Pimoroni [1.12" OLED Breakout](https://shop.pimoroni.com/products/1-12-oled-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install all of the required libraries.

## Running this example

To run this example, type `./uv-warning.py` in the terminal

## Notes

You might want rotate your Pi and Breakout Garden so that the UV sensor is facing 
upwards at a better angle to detect UV light.
