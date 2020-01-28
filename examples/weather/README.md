# Weather example

This example turns your Breakout Garden into a mini weather display
combining indoor temperature and pressure data with a weather icon
indicating the current local weather conditions.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat-i2c-spi)
- A Pimoroni [BME680 Breakout](https://shop.pimoroni.com/products/bme680-breakout)
- A Pimoroni [1.12" OLED Breakout (SPI)](https://shop.pimoroni.com/products/1-12-oled-breakout)

You'll need the requests (`sudo pip install requests`), geocoder (`sudo pip install geocoder`), 
and BeautifulSoup4 (`sudo pip install beautifulsoup4`) libraries to query the Dark Sky weather page.

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install the libraries to run the I2C breakouts.

For this example you'll need to make sure some additional software is installed:

```
sudo apt install python3-lxml python3-pil
sudo pip3 install requests geocoder beautifulsoup4
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

To run this example, type `./weather.py` in the terminal

## Notes

This example uses Sheffield as the default location, so you'll need to specify your city and 
country code at the top of the file, changing the variables called `CITY` and `COUNTRYCODE` 
to your current location.
