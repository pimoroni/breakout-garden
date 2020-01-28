# Seismograph example

The Dino-Detect v1.2 beta is a dino stomp detector. It's a
UNIX system, I know this.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat-i2c-spi)
- A Pimoroni [LSM303D 6DoF Sensor Breakout](https://shop.pimoroni.com/products/lsm303d-6dof-motion-sensor-breakout)
- A Pimoroni [1.12" OLED Breakout (SPI)](https://shop.pimoroni.com/products/1-12-oled-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install the libraries to run the I2C breakouts.

For this example you'll need to make sure some additional software is installed:

```
sudo apt install python3-pil
```

You'll need to clone and install the library for the 1.12" OLED Breakout (SPI)
as follows:

```
git clone https://github.com/pimoroni/sh1106-python
sudo ./install.sh
```

This example assumes that you have the OLED plugged into the front slot on the
Breakout Garden HAT, which should also work with the Breakout Garden Mini HAT.
To change it to the back slot, change `device=1` to `device=0` on the line 
where the OLED is set up. 

## Running this example

To run this example, type `./seismograph.py` in the terminal.

Note that it takes a baseline reading initially to zero out the axes,
and then calculates subsequent readings against the baseline, so make
sure that your Breakout Garden is sitting still when you start the
program.

The `sensitivity` variable can be changed to make the seismograph more or
less sensitive to dino stomps.
