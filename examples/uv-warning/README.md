# UV warning example

This example uses a VEML6075 UVA/B sensor, a 5x5 RGB matrix, and a 1.2" OLED breakout
to display average UV index as a traffic light warning on the RGB matrix, with green
being a low UV index, yellow/orange being moderate, and red high or extreme. The numerical
values and a descriptive warning are displayed on the OLED.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat-i2c-spi)
- A Pimoroni [VEML6075 UVA/B Sensor Breakout Breakout](https://shop.pimoroni.com/products/veml6075-uva-b-sensor-breakout)
- A Pimoroni [5x5 RGB Matrix Breakout](https://shop.pimoroni.com/products/5x5-rgb-matrix-breakout)
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

To run this example, type `./uv-warning.py` in the terminal

## Notes

You might want rotate your Pi and Breakout Garden so that the UV sensor is facing 
upwards at a better angle to detect UV light.
