#!/usr/bin/env python3

import time

import automationhat

print("""
Press CTRL+C to exit.
""")

while True:
    one = automationhat.analog.one.read()
    two = automationhat.analog.two.read()
    print(one, two)
    time.sleep(0.5)
