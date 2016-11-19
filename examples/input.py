#!/usr/bin/env python

import time

import automationhat


if automationhat.is_automation_hat():
    automationhat.light.power.write(1)

while True:
    print(automationhat.input.read())
    print(automationhat.analog.read())
    time.sleep(0.5)
