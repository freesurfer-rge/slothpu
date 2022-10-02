import urwid

from slothpu import Memory

class MemoryColumn(urwid.WidgetWrap):
    def __init__(self, memory_area: Memory):
        self._memory = memory_area