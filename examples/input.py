import automationhat as ah
import time

ah.light.power.write(1)

while True:
    print(ah.input.read())
    print(ah.analog.read())
    time.sleep(0.5)
