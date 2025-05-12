#!/usr/bin/env python3
"""
Control servos for waste-bin lids using GPIOZero on a Raspberry Pi.
Each class name in data/labels.txt is mapped to a GPIO pin.
On non-Pi environments, falls back to no-op stubs for local testing.
"""
import time

# Attempt to import GPIOZero; if missing, provide a stub for local testing
try:
    from gpiozero import Servo
    _use_gpio = True
except ImportError:
    _use_gpio = False
    class Servo:
        def __init__(self, *args, **kwargs): pass
        def max(self): pass
        def min(self): pass

# Map classification names to GPIO pins (Pi only)
PIN_MAP = {
    "trash":        17,
    "recycle":      27,
    "compost":      22,
    "electronics":  23
}

# Initialize servos with appropriate pulse widths for SG90s
SERVOS = {
    cls: Servo(pin, min_pulse_width=0.5/1000, max_pulse_width=2.4/1000)
    for cls, pin in PIN_MAP.items()
}

def pick_bin(cls_name: str) -> None:
    """
    Open the lid for the given class by moving the servo, then close it.
    Falls back to no-op if GPIO is unavailable.
    """
    servo = SERVOS.get(cls_name)
    if not servo:
        return
    # Open lid
    servo.max()
    time.sleep(1.0)
    # Close lid
    servo.min()
