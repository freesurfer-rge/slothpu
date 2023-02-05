# Loopback tests of the TesterBoard

import random

import pytest

from tester_board import TesterBoard


def test_all_on():
    tb = TesterBoard()

    all_on = [True for _ in range(tb.n_pins)]

    tb.send(all_on)

    received = tb.recv()

    assert received == all_on


def test_all_off():
    tb = TesterBoard()

    all_off = [False for _ in range(tb.n_pins)]

    tb.send(all_off)

    received = tb.recv()

    assert received == all_off


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 7, 8, 9, 10])
def test_every_n(n: int):
    tb = TesterBoard()

    inputs = [i % n == 0 for i in range(tb.n_pins)]

    tb.send(inputs)

    received = tb.recv()

    assert inputs == received


@pytest.mark.parametrize("p_true", [0.1, 0.2, 0.5, 0.7, 0.8, 0.9])
def test_random(p_true: float):
    tb = TesterBoard()

    random.seed()
    for _ in range(100):
        inputs = random.choices(
            population=[False, True], weights=[1 - p_true, p_true], k=tb.n_pins
        )
        tb.send(inputs)
        received = tb.recv()

        assert inputs == received


def test_smoke_output_enable():
    tb = TesterBoard()

    all_on = [True for _ in range(tb.n_pins)]
    tb.send(all_on)

    # Assert everything as expected
    received = tb.recv()
    assert received == all_on

    all_off = [False for _ in range(tb.n_pins)]
    # Disable all outputs
    tb.enable_outputs([False, False, False, False, False])
    received = tb.recv()
    assert received == all_off  # Have pull downs

    # Enable all outputs
    tb.enable_outputs([True, True, True, True, True])
    received = tb.recv()
    assert received == all_on


@pytest.mark.parametrize("i_bank", range(5))
def test_output_disable_by_bank(i_bank):
    tb = TesterBoard()
    PINS_PER_BANK = 8  # on each 595

    all_on = [True for _ in range(tb.n_pins)]
    tb.send(all_on)

    # Assert everything as expected
    received = tb.recv()
    assert received == all_on

    enable_banks = [True for _ in range(5)]
    enable_banks[i_bank] = False
    tb.enable_outputs(enable_banks)

    received = tb.recv()
    for i in range(tb.n_pins):
        assert received[i] == (i // PINS_PER_BANK != i_bank)


@pytest.mark.parametrize("i_bank", range(5))
def test_output_enable_by_bank(i_bank):
    tb = TesterBoard()
    PINS_PER_BANK = 8  # on each 595

    all_on = [True for _ in range(tb.n_pins)]
    tb.send(all_on)

    # Assert everything as expected
    received = tb.recv()
    assert received == all_on

    enable_banks = [False for _ in range(5)]
    enable_banks[i_bank] = True
    tb.enable_outputs(enable_banks)

    received = tb.recv()
    for i in range(tb.n_pins):
        assert received[i] == (i // PINS_PER_BANK == i_bank)
