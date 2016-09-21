#!/usr/bin/env python

import time

import automationhat as autohat


autohat.light.power.write(1)

while True:
    autohat.relay.one.toggle()
    autohat.relay.two.toggle()
    autohat.relay.three.toggle()
    time.sleep(0.1)
