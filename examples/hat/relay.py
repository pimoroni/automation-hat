#!/usr/bin/env python3

import time

import automationhat

if automationhat.is_automation_hat():
    automationhat.light.power.write(1)

while True:
    automationhat.relay.one.toggle()
    if automationhat.is_automation_hat():
        automationhat.relay.two.toggle()
        automationhat.relay.three.toggle()
    time.sleep(0.1)
