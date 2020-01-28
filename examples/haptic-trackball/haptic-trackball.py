#!/usr/bin/env python3

import time
from trackball import TrackBall
from drv2605 import DRV2605


print("""This Pimoroni Breakout Garden example requires a
DRV2605L Haptic Breakout and a Trackball Breakout.

This example demonstrates how to generate haptic feedback
as the trackball is scrolled/pressed.

Press Ctrl+C to exit.
""")


# Set up Trackball Breakout.
trackball = TrackBall(interrupt_pin=4)
drv2605 = DRV2605()

x = 0
y = 0

delta_x = 0
delta_y = 0
last_state = 0

# Set up Haptic Breakout.
drv2605.reset()
drv2605.set_realtime_data_format('Unsigned')
drv2605.set_feedback_mode('LRA')
drv2605.set_mode('Real-time Playback')
drv2605.go()

try:
    while True:
        # Get positional values from trackball.
        up, down, left, right, switch, state = trackball.read()
        y += up
        y -= down
        x += right
        x -= left

        delta_x += right
        delta_x -= left

        delta_y += up
        delta_y -= down

        x = max(0, min(x, 255))
        y = max(0, min(y, 255))

        # Generate a longer click when trackball is pressed.
        if state != last_state:
            drv2605.set_realtime_input(255)
            time.sleep(0.01)
            drv2605.set_realtime_input(0)
            last_state = state

        # Generate shorter clicks when trackball is scrolled.
        if abs(delta_x) > 2:
            drv2605.set_realtime_input(255)
            time.sleep(0.005)
            drv2605.set_realtime_input(0)
            delta_x = 0

        elif abs(delta_y) > 2:
            drv2605.set_realtime_input(255)
            time.sleep(0.005)
            drv2605.set_realtime_input(0)
            delta_y = 0

        time.sleep(0.001)

except KeyboardInterrupt:
    pass
