# Weather example

This example turns your Breakout Garden into a mini weather display
combining indoor temperature and pressure data with a weather icon
indicating the current local weather conditions.

## Pre-requisites

This example requires:

- A Pimoroni [Breakout Garden](https://shop.pimoroni.com/products/breakout-garden-hat)
- A Pimoroni [BME680 Breakout](https://shop.pimoroni.com/products/bme680-breakout)
- A Pimoroni [1.12" OLED Breakout](https://shop.pimoroni.com/products/1-12-oled-breakout)

You'll need the requests (`sudo pip install requests`), geocoder (`sudo pip install geocoder`), and BeautifulSoup4 (`sudo pip install beautifulsoup4`) libraries to query the Dark Sky weather page.

## Installation

Pop the breakouts into your Breakout Garden, and then run the `install.sh`
script in the root of this repository with `sudo ./install.sh` to automagically
install all of the required libraries.

## Running this example

To run this example, type `./weather.py` in the terminal

## Notes

This example uses Sheffield as the default location, so you'll need to specify your city and country code at the top of the file, changing the variables called `CITY` and `COUNTRYCODE` to your current location.
