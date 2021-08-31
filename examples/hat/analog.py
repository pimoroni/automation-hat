#!/usr/bin/env python3

import time

import automationhat

# For Automation HAT before September 2021
automationhat.ADC.select(automationhat.ADC_ADS1015)

# For Automation HAT after September 2021
# automationhat.ADC.select(automationhat.ADC_ADS1115)

print("""
Press CTRL+C to exit.
""")

while True:
    value1 = automationhat.analog.one.read()
    value2 = automationhat.analog.two.read()
    print(value1, value2)
    time.sleep(0.25)
