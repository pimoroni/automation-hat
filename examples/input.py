#!/usr/bin/env python

import time

import automationhat


if len(automationhat.light) > 0:
    automationhat.light.power.write(1)

while True:
    print(automationhat.input.read())
    print(automationhat.analog.read())
    time.sleep(0.5)
