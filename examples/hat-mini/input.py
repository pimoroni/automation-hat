#!/usr/bin/env python3

import sys
import time

import automationhat

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

import st7735

print("""input.py

This Automation HAT Mini example displays the status of
the three 24V-tolerant digital inputs.

Press CTRL+C to exit.
""")

# Create ST7735 LCD display class.
disp = st7735.ST7735(
    port=0,
    cs=st7735.BG_SPI_CS_FRONT,
    dc=9,
    backlight=25,
    rotation=270,
    spi_speed_hz=4000000
)

# Initialize display.
disp.begin()

on_colour = (99, 225, 162)
off_colour = (235, 102, 121)

# Values to keep everything aligned nicely.
on_x = 115
on_y = 35

off_x = 46
off_y = on_y

dia = 10

while True:
    # Value to increment for spacing circles vertically.
    offset = 0

    # Open our background image.
    image = Image.open("images/inputs-blank.jpg")
    draw = ImageDraw.Draw(image)

    # Draw the circle for each channel in turn.
    for channel in range(3):
        if automationhat.input[channel].is_on():
            draw.ellipse((on_x, on_y + offset, on_x + dia, on_y + dia + offset), on_colour)
        elif automationhat.input[channel].is_off():
            draw.ellipse((off_x, off_y + offset, off_x + dia, off_y + dia + offset), off_colour)

        offset += 14

    # Draw the image to the display
    disp.display(image)

    time.sleep(0.25)
