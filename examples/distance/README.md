# Distance example

This example, the Park-O-Matic 6000, is a mockup of a car reversing
indicator.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat)
- A Pimoroni [VL53L1X Time of Flight Sensor Breakout](https://shop.pimoroni.com/products/vl53l1x-breakout)
- A Pimoroni [1.12" OLED Breakout](https://shop.pimoroni.com/products/1-12-oled-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install all of the required libraries.

## Running this example

To run this example, type `./distance.py` in the terminal.

You can change the `threshold` value (in cm) to change the threshold at which the warning
indicator starts flashing.

## Notes

You can add (or edit) the line `dtparam=i2c_arm_baudrate=1000000` at the bottom 
of your `/boot/config.txt` file to speed up your I2C a bit and improve the speed 
of this example.
