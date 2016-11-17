#!/usr/bin/env python

import time

import automationhat


if len(automationhat.light) > 0:
    automationhat.light.power.write(1)

while True:
    automationhat.relay.one.toggle()
    if len(automationhat.relay) > 1:
        automationhat.relay.two.toggle()
        automationhat.relay.three.toggle()
    time.sleep(0.1)
