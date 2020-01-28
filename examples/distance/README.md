# Distance example

This example, the Park-O-Matic 6000, is a mockup of a car reversing
indicator.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat-i2c-spi)
- A Pimoroni [VL53L1X Time of Flight Sensor Breakout](https://shop.pimoroni.com/products/vl53l1x-breakout)
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

To run this example, type `./distance.py` in the terminal.

You can change the `threshold` value (in cm) to change the threshold at which the warning
indicator starts flashing.
