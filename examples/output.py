#!/usr/bin/env python

import time

import automationhat as autohat


autohat.light.power.write(1)

while True:
    autohat.light.comms.toggle()
    autohat.light.warn.toggle()
    autohat.relay.one.toggle()
    autohat.relay.two.toggle()
    autohat.relay.three.toggle()
    autohat.output.toggle()
    print(autohat.analog.read())
    time.sleep(0.5)
