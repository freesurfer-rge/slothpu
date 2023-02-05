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
