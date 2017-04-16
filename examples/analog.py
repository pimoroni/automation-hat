#!/usr/bin/env python

import time

import automationhat
time.sleep(0.1) # short pause after ads1015 class creation recommended


print("""
Press CTRL+C to exit.
""")

while True:
    value = automationhat.analog.one.read()
    print(value)
    time.sleep(0.25)
