import automationhat as ah
import time

ah.light.power.write(1)

while True:
    ah.light.comms.toggle()
    ah.relay.one.toggle()
    ah.relay.two.toggle()
    ah.relay.three.toggle()
    ah.output.toggle()
    print(ah.analog.read())
    time.sleep(0.5)
