#!/usr/bin/env python

import time
import signal

import automationhat

automationhat.enable_auto_lights(False)

automationhat.light.on()

for analog in automationhat.analog:
    analog.light.on()

for output in automationhat.output:
    output.light.on()

for input in automationhat.input:
    input.light.on()

signal.pause()
