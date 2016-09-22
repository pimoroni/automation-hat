#!/usr/bin/env python

import time

import automationhat as autohat


autohat.light.power.write(1)

while True:
    print(autohat.input.read())
    print(autohat.analog.read())
    time.sleep(0.5)
