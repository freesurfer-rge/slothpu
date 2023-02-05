import RPi.GPIO as GPIO

import logging
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.setLevel(logging.INFO)

GPIO.setmode(GPIO.BOARD)


oe_pins = [15, 13, 7, 5, 3]

clk_out = 23
copi = 19
out_select = 24

for oe_pin in oe_pins:
    logger.info(f"Configuring {oe_pin}")
    GPIO.setup(oe_pin, GPIO.OUT)
    GPIO.output(oe_pin, GPIO.LOW)

GPIO.setup(clk_out, GPIO.OUT)
GPIO.setup(copi, GPIO.OUT)
GPIO.setup(out_select, GPIO.OUT)

GPIO.output(out_select, GPIO.LOW)

for i in reversed(range(40)):
    if i in [7, 9, 11]:
        GPIO.output(copi, GPIO.LOW)
    else:
        GPIO.output(copi, GPIO.HIGH)
    GPIO.output(clk_out, GPIO.LOW)
    GPIO.output(clk_out, GPIO.HIGH)
GPIO.output(clk_out, GPIO.LOW)
GPIO.output(out_select, GPIO.HIGH)

time.sleep(10)

GPIO.cleanup()
