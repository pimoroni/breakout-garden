#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE! This code should not be used for medical diagnosis. It's
# for fun/novelty use only, so bear that in mind while using it.

import sys
import time

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from threading import Thread
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106

from max30105 import MAX30105, HeartRate

print("""
NOTE! This code should not be used for medical diagnosis. It's
for fun/novelty use only, so bear that in mind while using it.

This Pimoroni Breakout Garden example requires a
MAX30105 Breakout and a 1.12" OLED Breakout.

The Pulse-O-Matic 6000 is a heartbeat plotter and BPM display.

Press Ctrl+C a couple times to exit.
""")

# Set up OLED
oled = sh1106(i2c(port=1, address=0x3C), rotate=2, height=128, width=128)

# Load fonts
lsb_18 = ImageFont.truetype("fonts/LiberationSans-Bold.ttf", 18)
lsr_12 = ImageFont.truetype("fonts/LiberationSans-Regular.ttf", 12)

# Set up MAX30105 Breakout
max30105 = MAX30105()
max30105.setup(leds_enable=2)

max30105.set_led_pulse_amplitude(1, 0.2)
max30105.set_led_pulse_amplitude(2, 12.5)
max30105.set_led_pulse_amplitude(3, 0)

max30105.set_slot_mode(1, 'red')
max30105.set_slot_mode(2, 'ir')
max30105.set_slot_mode(3, 'off')
max30105.set_slot_mode(4, 'off')

hr = HeartRate(max30105)
data = []
running = True

bpm = 0
bpm_avg = 0
beat_detected = False
beat_status = False


def sample():
    """Function to thread accelerometer values separately to
 OLED drawing"""
    global bpm, bpm_avg, beat_detected, beat_status

    average_over = 5
    bpm_vals = [0 for x in range(average_over)]
    last_beat = time.time()

    while running:
        t = time.time()
        samples = max30105.get_samples()
        if samples is not None:
            for i in range(0, len(samples), 2):
                ir = samples[i + 1]
                beat_detected = hr.check_for_beat(ir)
                if beat_detected:
                    beat_status = True
                    delta = t - last_beat
                    last_beat = t
                    bpm = 60 / delta
                    bpm_vals = bpm_vals[1:] + [bpm]
                    bpm_avg = sum(bpm_vals) / average_over
                d = hr.low_pass_fir(ir & 0xff)
                data.append(d)
                if len(data) > 128:
                    data.pop(0)

        time.sleep(0.05)


# The thread to measure acclerometer values
t = Thread(target=sample)
t.start()

# The main loop that draws values to the OLED
while True:
    try:
        img = Image.open("images/heartbeat.png").convert(oled.mode)
        draw = ImageDraw.Draw(img)

        # Draw the heartbeat trace
        vals = data
        new_vals = [x / float((max(vals) - min(vals))) * 32 for x in vals]

        for i in range(1, len(new_vals)):
            draw.line([(i - 1, 80 - new_vals[i - 1]), (i, 80 - new_vals[i])],
                      fill="white")

        # Draw the Pulse-O-Matic "branding"
        draw.rectangle([(0, 0), (128, 20)], fill="black")
        if bpm_avg > 40:
            draw.text((0, 1), "BPM: {:.2f}".format(bpm_avg), fill="white",
                      font=lsb_18)
        else:
            draw.text((0, 1), "BPM: --.--", fill="white", font=lsb_18)
        if beat_status:
            draw.text((115, 1), u"\u2665", fill="white", font=lsb_18)
            beat_status = False
        draw.line([(0, 20), (128, 20)], fill="white")

        draw.rectangle([(0, 108), (128, 128)], fill="black")
        draw.text((0, 110), "Pulse-O-Matic 6000", fill="white", font=lsr_12)
        draw.line([(0, 108), (128, 108)], fill="white")

        # Display on the OLED
        oled.display(img)
    except ZeroDivisionError:
        pass
    except KeyboardInterrupt:
        running = False
        sys.exit(0)
