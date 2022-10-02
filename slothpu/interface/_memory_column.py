import urwid

from slothpu import Memory


class MemoryColumn(urwid.ListBox):
    def __init__(self, memory_area: Memory):
        self._memory = memory_area

        self._memory_walker = urwid.SimpleListWalker(
            [
                urwid.Text(self.get_string_for_location(i))
                for i in range(len(self._memory))
            ]
        )

        super(MemoryColumn, self).__init__(self._memory_walker)

    def get_string_for_location(self, i):
        return f"{i:3} : {self._memory.get_as_string(i)}"

    def update(self):
        for i in range(len(self._memory)):
            nxt = self._memory_walker.contents[i]
            nxt.set_text(self.get_string_for_location(i))
