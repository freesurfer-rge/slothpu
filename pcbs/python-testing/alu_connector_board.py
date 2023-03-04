from typing import List

from tester_board import TesterBoard

class ALUConnectorBoard:
    def __init__(self):
        """Initialise with an internal TesterBoard."""
        self._tb = TesterBoard()

        # Enable all outputs
        self._tb.enable_outputs([True for _ in range(5)])

    @property
    def A_bus(self) -> List[int]:
        return [31, 29, 27, 25, 23, 21, 19, 17]

    @property
    def B_bus(self) -> List[int]:
        return [15, 13, 11, 9, 7, 5, 3, 1]

    @property
    def I(self) -> List[int]:
        return [33, 35, 37, 39]

    @property
    def Commit(self) -> int:
        return 32

    @property
    def Execute(self) -> int:
        return 34
