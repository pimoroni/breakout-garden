# Spirit level example

This examples emulates a circular spirit level, using the
LCD to draw the spirit level and the accelerometer to
detect orientation.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat-i2c-spi)
- A Pimoroni [MSA301 3DoF Motion Sensor Breakout](https://shop.pimoroni.com/products/msa301-3dof-motion-sensor-breakout)
- A Pimoroni [1.3" LCD Breakout](https://shop.pimoroni.com/products/1-3-spi-colour-lcd-240x240-breakout)

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install the libraries to run the I2C breakouts.

For this example you'll need to make sure some additional software is installed:

```
sudo apt install python3-pil
```

You'll need to clone and install the library for the 1.3" LCD Breakout
as follows:

```
git clone https://github.com/pimoroni/st7789-python
cd library
sudo python3 setup.py install
```

This example assumes that you have the LCD plugged into the front slot on the
Breakout Garden HAT, which should also work with the Breakout Garden Mini HAT.
To change it to the back slot, change `cs=ST7789.BG_SPI_CS_FRONT` to 
`cs=ST7789.BG_SPI_CS_BACK` and `backlight=19` to backlight=18` on the line 
where the LCD is set up. 

## Running this example

To run this example, type `./spirit-level.py` in the terminal.
