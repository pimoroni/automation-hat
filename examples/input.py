#!/usr/bin/env python

import time

import automationhat

""" Example use of internal resistor from the Pi
If we want to use the Pi's internal resistors for our digital inputs, we
need to configure this BEFORE we initialize our board.

The resistor can be activited for each of the 3 digital inputs separately.
The could be set to either
    automationhat.PULL_DOWN -> which means the default will be 0 until connected to VCC
    automationhat.PULL_UP -> which means the default will be 1 until connected to GND
"""
automationhat.input.three.resistor(automationhat.PULL_DOWN)

if automationhat.is_automation_hat():
    automationhat.light.power.write(1)

while True:
    print(automationhat.input.read())
    print(automationhat.analog.read())
    time.sleep(0.5)
