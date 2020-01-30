#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
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
bubble_dia = 64
bubble_rad = bubble_dia / 2
circle_dia = 190
circle_rad = circle_dia / 2
border = (WIDTH - circle_dia) / 2

centre_x = WIDTH / 2
centre_y = HEIGHT / 2

# Set up MSA301
accel = msa301.MSA301()
accel.set_power_mode('normal')

while True:
    # Read MSA301 values
    x, y, z = accel.get_measurements()

    # z = x-axis, y = y-axis
    bubble_centre_x = (2 - (z + 1)) * (circle_dia / 2) + border
    bubble_centre_y = (y + 1) * (circle_dia / 2) + border

    # Work out vector length to check if outside circle
    delta_x = bubble_centre_x - centre_x
    delta_y = bubble_centre_y - centre_y

    vector_length = math.sqrt(delta_x ** 2 + delta_y ** 2)

    # If outside circle, scale position back down relatively
    if vector_length > circle_rad - bubble_rad:
        scale = (circle_rad - bubble_rad) / vector_length
        bubble_centre_x = centre_x + delta_x * scale
        bubble_centre_y = centre_y + delta_y * scale

    # Use red crosshair if bubble is close to centre
    if (-0.05 < z < 0.05) and (-0.05 < y < 0.05):
        crosshair = crosshair_red
    else:
        crosshair = crosshair_black

    # Construct image
    image = Image.new('RGBA', (WIDTH, HEIGHT), color=(0, 0, 0, 0))
    image.paste(level, (0, 0))
    image.paste(bubble, (int(bubble_centre_x - (bubble_dia / 2)), int(bubble_centre_y  - (bubble_dia / 2))), mask=bubble)
    image.paste(crosshair, (0, 0), mask=crosshair)

    # Display on LCD
    disp.display(image)
