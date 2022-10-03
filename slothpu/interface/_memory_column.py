import urwid

from slothpu import Memory


class MemoryColumn(urwid.ListBox):
    def __init__(self, memory_area: Memory):
        self.head = urwid.Text("Main Memory")

        self._memory = memory_area

        self._memory_items = [
            urwid.Text(self.get_string_for_location(i))
            for i in range(len(self._memory))
        ]

        slw = urwid.SimpleListWalker(self._memory_items)

        super(MemoryColumn, self).__init__(slw)

    def get_string_for_location(self, i):
        return f"{i:3} : {self._memory.get_as_string(i)}"

    def update(self):
        for i in range(len(self._memory)):
            self._memory_items[i].set_text(self.get_string_for_location(i))
