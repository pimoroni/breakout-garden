# Heartbeat example

# Important

**This code should not be used for medical diagnosis, as the basis for a real smoke
or fire detector, or in life-critical situations. It's for fun/novelty use only, 
so bear that in mind while using it.**

This example, the Pulse-O-Matic 6000, is a heartbeat plotter and BPM display.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat)
- A Pimoroni [MAX30105 Breakout - Heart Rate, Oximeter, Smoke Sensor](https://shop.pimoroni.com/products/max30105-breakout-heart-rate-oximeter-smoke-sensor)
- A Pimoroni [1.12" OLED Breakout](https://shop.pimoroni.com/products/1-12-oled-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install all of the required libraries.

## Running this example

To run this example, type `./heartbeat.py` in the terminal.

It's best to hold the sensor against your fingertip (the fleshy side)
using a piece of wire or a rubber band looped through the mounting
holes on the breakout, as the sensor is very sensitive to small
movements and it's hard to hold your finger against the sensor with
even pressure.

If you're using your MAX30105 Breakout with Breakout Garden, then
we'd recommend using one of our 
[Breakout Garden Extender Kits](https://shop.pimoroni.com/products/breakout-garden-extender-kit)
with some [female to female jumper jerky](https://shop.pimoroni.com/products/jumper-jerky?variant=348491271).

## Notes

You can add (or edit) the line `dtparam=i2c_arm_baudrate=1000000` at the bottom 
of your `/boot/config.txt` file to speed up your I2C a bit and improve the speed 
of this example.
