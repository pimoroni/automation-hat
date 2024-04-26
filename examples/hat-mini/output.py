#!/usr/bin/env python3

import os
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

IMAGE_PATH = os.path.join(os.path.dirname(__file__), "images")

print("""output.py

This Automation HAT Mini example toggles and displays the
status of the three 24V-tolerant digital outputs.

Press CTRL+C to exit.
""")

def draw_states(channels):
    # Open our background image.
    image = Image.open(os.path.join(IMAGE_PATH, "outputs-blank.jpg"))
    draw = ImageDraw.Draw(image)
    offset = 0

    # Draw the on/off state of each channel.
    for channel in range(len(channels)):
        if channels[channel].is_on():
            draw.ellipse((on_x, on_y + offset, on_x + dia, on_y + dia + offset), on_colour)

        else:
            draw.ellipse((off_x, off_y + offset, off_x + dia, off_y + dia + offset), off_colour)
        offset += 14

    disp.display(image)


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
bg_colour = (25, 16, 45)

# Values to keep everything aligned nicely.
on_x = 115
on_y = 35

off_x = 46
off_y = on_y

dia = 10

while True:
    for channel in range(3):
        for state in range(2):
            # Toggle channel.
            automationhat.output[channel].write(state)

            # Draw the states to the display.
            draw_states(automationhat.output())

            # Pause.
            time.sleep(0.5)

            # Toggle channel back.
            automationhat.output[channel].write(1 - state)
