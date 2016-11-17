#!/usr/bin/env python

import time

import automationhat


if len(automationhat.light) > 0:
    automationhat.light.power.write(1)

while True:
    if len(automationhat.light) > 0:
        automationhat.light.comms.toggle()
        automationhat.light.warn.toggle()
    
    automationhat.relay.one.toggle()
    
    if len(automationhat.relay) > 1:
        automationhat.relay.two.toggle()
        automationhat.relay.three.toggle()
    
    automationhat.output.toggle()
    
    print(automationhat.analog.read())
    
    time.sleep(0.5)
