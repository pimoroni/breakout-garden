# Seismograph example

The Dino-Detect v1.2 beta is a dino stomp detector. It's a
UNIX system, I know this.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat)
- A Pimoroni [LSM303D 6DoF Sensor Breakout](https://shop.pimoroni.com/products/lsm303d-6dof-motion-sensor-breakout)
- A Pimoroni [1.12" OLED Breakout](https://shop.pimoroni.com/products/1-12-oled-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install all of the required libraries.

## Running this example

To run this example, type `./seismograph.py` in the terminal.

Note that it takes a baseline reading initially to zero out the axes,
and then calculates subsequent readings against the baseline, so make
sure that your Breakout Garden is sitting still when you start the
program.

The `sensitivity` variable can be changed to make the seismograph more or
less sensitive to dino stomps.

## Notes

You can add (or edit) the line `dtparam=i2c_arm_baudrate=1000000` at the bottom 
of your `/boot/config.txt` file to speed up your I2C a bit and improve the speed 
of this example.
