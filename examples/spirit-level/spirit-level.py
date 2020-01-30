#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import msa301
import ST7789 as ST7789

print("""This Pimoroni Breakout Garden example requires an
MSA301 3DoF Motion Sensor Breakout and a 1.3" LCD Breakout.

This examples emulates a circular spirit level, using the
LCD to draw the spirit level and the accelerometer to
detect orientation.

Press Ctrl+C to exit.
""")

# Set up LCD
disp = ST7789.ST7789(
    port=0,
    cs=ST7789.BG_SPI_CS_FRONT,
    dc=9,
    backlight=19,
    spi_speed_hz=80 * 1000 * 1000
)

WIDTH = disp.width
HEIGHT = disp.height

disp.begin()

# Load the image assets
level = Image.open("images/spirit-level.png").convert("RGBA")
bubble = Image.open("images/spirit-level-bubble.png").convert("RGBA")
crosshair_black = Image.open("images/spirit-level-crosshair-black.png").convert("RGBA")
crosshair_red = Image.open("images/spirit-level-crosshair-red.png").convert("RGBA")

# Sizes/coordinates of things
centre = (88, 88)
bubble_dia = 64
circle_dia = 190
border = (WIDTH - circle_dia) / 2

# Set up MSA301
accel = msa301.MSA301()
accel.set_power_mode('normal')

while True:
    # Read MSA301 values
    x, y, z = accel.get_measurements()

    # z = x-axis, y = y-axis
    x_level = (2 - (z + 1)) * (circle_dia / 2) + border - (bubble_dia / 2)
    y_level = (y + 1) * (circle_dia / 2) + border - (bubble_dia / 2)

    # Clamp to bounds of green circle
    x_level = min(WIDTH - border - bubble_dia, max(border, x_level))
    y_level = min(WIDTH - border - bubble_dia,max(border, y_level))

    # Use red crosshair if bubble is close to centre
    if (-0.05 < z < 0.05) and (-0.05 < y < 0.05):
        crosshair = crosshair_red
    else:
        crosshair = crosshair_black

    # Construct image
    image = Image.new('RGBA', (WIDTH, HEIGHT), color=(0, 0, 0, 0))
    image.paste(level, (0, 0))
    image.paste(bubble, (int(x_level), int(y_level)), mask=bubble)
    image.paste(crosshair, (0, 0), mask=crosshair)

    # Display on LCD
    disp.display(image)
