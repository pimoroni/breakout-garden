#!/bin/env python

import time
from ltr559 import setup, update_sensor, get_lux, get_proximity
from rgbmatrix5x5 import RGBMatrix5x5

print("""This Pimoroni Breakout Garden example requires an
LTR-559 Light and Proximity Breakout and a 5x5 RGB Matrix Breakout.
This example creates a little nightlight that can be toggled on or
off by tapping the proximity sensor with your finger, or triggered
automatically when it's dark. Press Ctrl+C a couple times to exit.
""")

# Set up the LTR-559 sensor
setup()

# Set up the 5x5 RGB matrix
rgbmatrix5x5 = RGBMatrix5x5()
rgbmatrix5x5.set_clear_on_exit()
rgbmatrix5x5.set_brightness(0.8)

# Initial variables to keep track of state of light
state = False
last_state = False
toggled = False

light_threshold = 100  # Low-light trigger level
prox_threshold = 1000  # Proximity trigger level
colour = (255, 165, 0)  # Orange-ish


# Function to toggle the RGB matrix on or off depending on state
def toggle_matrix():
    global state, last_state

    if state is True and last_state is False:
        rgbmatrix5x5.set_all(*colour)
        rgbmatrix5x5.show()
    elif state is False and last_state is True:
        rgbmatrix5x5.clear()
        rgbmatrix5x5.show()

    last_state = state


# Read the sensor once, as the first values are always squiffy
update_sensor()
lux = get_lux()
prox = get_proximity()
time.sleep(1)

try:
    while True:
        # Read the light and proximity sensor
        update_sensor()
        lux = get_lux()
        prox = get_proximity()

        # If it's dark and the light isn't toggled on, turn on
        if lux < light_threshold and not toggled:
            state = True
            if state != last_state:
                print("It's dark! Turning light ON")
            toggle_matrix()

        # If it's light and the light isn't on, turn off
        elif lux >= light_threshold and not toggled:
            state = False
            if state != last_state:
                print("It's light! Turning light OFF")
            toggle_matrix()

        # If there's a tap on the sensor
        if prox > prox_threshold:
            # Toggle it off if it's currently on
            if toggled:
                state = False
                toggled = False
                if state != last_state:
                    print("Toggling light OFF")
                toggle_matrix()
            # Toggle it on if it's currently off
            else:
                state = True
                toggled = True
                if state != last_state:
                    print("Toggling light ON")
                toggle_matrix()
            # Debounce to stop retriggering
            time.sleep(0.5)

        elif prox < prox_threshold and lux >= light_threshold:
            state = False

        time.sleep(0.05)

except KeyboardInterrupt:
    pass
