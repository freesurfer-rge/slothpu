import urwid

from slothpu import MainMemory


class MemoryColumn(urwid.ListBox):
    def __init__(self, main_memory: MainMemory):
        self.head = urwid.Text("Main Memory")

        self._main_memory = main_memory

        self._memory_items = [
            urwid.Text(self.get_string_for_location(i))
            for i in range(len(self._main_memory.memory))
        ]

        slw = urwid.SimpleListWalker(self._memory_items)

        super(MemoryColumn, self).__init__(slw)

    def get_string_for_location(self, i: int):
        return f"{i:3} : {self._main_memory.memory.get_as_string(i)}"

    def update(self):
        for i in range(len(self._main_memory.memory)):
            self._memory_items[i].set_text(self.get_string_for_location(i))
