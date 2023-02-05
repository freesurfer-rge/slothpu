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
    if i in [21, 7, 9, 35]:
        GPIO.output(copi, GPIO.LOW)
    else:
        GPIO.output(copi, GPIO.HIGH)
    GPIO.output(clk_out, GPIO.LOW)
    GPIO.output(clk_out, GPIO.HIGH)
GPIO.output(clk_out, GPIO.LOW)
GPIO.output(out_select, GPIO.HIGH)

logger.info("Sleeping after output")
time.sleep(1)

clk_in = 40
in_select = 12
in_load = 37
cipo = 35


GPIO.setup(clk_in, GPIO.OUT)
GPIO.setup(in_load, GPIO.OUT)
GPIO.setup(in_select, GPIO.OUT)
GPIO.setup(cipo, GPIO.IN)

logger.info("Input configuration done")

logger.info("Loading the data")
GPIO.output(in_load, GPIO.HIGH)
GPIO.output(in_load, GPIO.LOW)
GPIO.output(in_load, GPIO.HIGH)

logger.info("Clocking data in")
GPIO.output(in_select, GPIO.LOW)
results = [0 for _ in range(40)]
for i in reversed(range(40)):
    results[i] = GPIO.input(cipo)
    GPIO.output(clk_in, GPIO.LOW)
    GPIO.output(clk_in, GPIO.HIGH)
GPIO.output(in_select, GPIO.HIGH)

for i in range(40):
    print(f"Output {i} : {results[i]}")

GPIO.cleanup()
