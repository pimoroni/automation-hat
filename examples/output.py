#!/usr/bin/env python

import time

import automationhat


if automationhat.is_automation_hat():
    automationhat.light.power.write(1)

while True:
    if automationhat.is_automation_hat():
        automationhat.light.comms.toggle()
        automationhat.light.warn.toggle()
    
    automationhat.relay.one.toggle()
    
    if automationhat.is_automation_hat():
        automationhat.relay.two.toggle()
        automationhat.relay.three.toggle()
    
    automationhat.output.toggle()
    
    print(automationhat.analog.read())
    
    time.sleep(0.5)
