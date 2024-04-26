#!/usr/bin/env python3

import sys
import time

import automationhat

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("""This example requires PIL.
Install with: sudo apt install python{v}-pil
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

import st7735

try:
    from fonts.ttf import RobotoBlackItalic as UserFont
except ImportError:
    print("""This example requires the Roboto font.
Install with: sudo pip{v} install fonts font-roboto
""".format(v="" if sys.version_info.major == 2 else sys.version_info.major))
    sys.exit(1)

print("""analog.py

This Automation HAT Mini example displays the three ADC
analog input voltages numerically and as bar charts.

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

# Initialise display.
disp.begin()

colour = (255, 181, 86)
font = ImageFont.truetype(UserFont, 12)

# Values to keep everything aligned nicely.
text_x = 110
text_y = 34

bar_x = 25
bar_y = 37
bar_height = 8
bar_width = 73

while True:
    # Value to increment for spacing text and bars vertically.
    offset = 0

    # Open our background image.
    image = Image.open("images/analog-inputs-blank.jpg")
    draw = ImageDraw.Draw(image)

    # Draw the text and bar for each channel in turn.
    for channel in range(3):
        reading = automationhat.analog[channel].read()
        draw.text((text_x, text_y + offset), "{reading:.2f}".format(reading=reading), font=font, fill=colour)

        # Scale bar dependent on channel reading.
        width = int(bar_width * (reading / 24.0))

        draw.rectangle((bar_x, bar_y + offset, bar_x + width, bar_y + bar_height + offset), colour)

        offset += 14

    # Draw the image to the display.
    disp.display(image)

    time.sleep(0.25)
