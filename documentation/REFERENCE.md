## Automation HAT / pHAT Function Reference

### Analog

Three of the four analog inputs on Automation HAT are 24V tolerant, with a forth 3.3V input in the breakout header.

The 24V tolerant inputs each have a basic voltage divider, using 120k and 820k resistors, that divides up to 25.85v down to the 0-3.3v range supported by the ADC. This slight over-range is compensated for in the library.

You can read an analog input like so:

```python
value = automationhat.analog.one.read()
```

### Inputs

The three inputs on Automation HAT are 24V tolerant, switching on at 3V and off at 1V. Behaviour at voltages between 1V and 3V is undefined.

The inputs are protected by a 20k resistor and 3.3v zener diode, limiting current to around 1mA.

You can read an input like so:

```python
state = automationhat.input.one.read()
```

### Outputs

The three outputs on Automation HAT are 24V tolerant, sinking outputs. That means you should connect them between your load and ground. They act like a switch down to ground, toggling your load on and off. The outputs are driven by a ULN2003A Darlington Array driver.

You can turn an output on like so:

```python
automationhat.output.one.on()
```

### Relays

The three relays on Automation HAT supply both NO (Normally Open) and NC (Normally Closed) terminals. You can use them to switch a single load, or alternate between two. The relays should be placed between the voltage supply and your load.

You can turn a relay on like so:

```python
automationhat.relay.one.on()
```

Or off:

```python
automationhat.relay.one.off()
```

Toggle it from its previous state:

```python
automationhat.relay.toggle()
```

Or write a specific value:

```python
automationhat.relay.write(1) # 1 = ON, 0 = OFF
```

### Lights

Automation HAT includes three user-controllable lights: Power, Comms and Warn. You can take control of these lights to turn them on/off or write a brightness value:

```python
automationhat.light.comms.on()
```

```python
automationhat.light.warn.off()
```

Note: lights use the same methods as relays and outputs: `on`, `off`, `toggle` and `write`.

Lights associated with Inputs, Outputs, Relays and Analog are automatic by default, but you can switch them to manual if you want. First turn off the automation:

```python
automationhat.analog.one.auto_light(False)
```

Then toggle the light:

```python
automationhat.analog.one.light.on()
automationhat.analog.one.light.off()
```
