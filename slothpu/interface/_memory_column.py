import urwid

from slothpu import Memory


class MemoryColumn(urwid.BoxWidget):
    def __init__(self, memory_area: Memory):
        self.head = urwid.Text("Main Memory")
        self.footer = urwid.Text("Footer")

        self._memory = memory_area

        self._memory_items = [
            urwid.Text(self.get_string_for_location(i))
            for i in range(len(self._memory))
        ]
        self.list_box = urwid.ListBox(urwid.SimpleListWalker(self._memory_items))
        self.frame = urwid.Frame(self.list_box, header=self.head)


    def render(self, size, focus=False):
        maxcol, maxrow = size
        head_rows = self.head.rows((maxcol,))
        if "bottom" in self.list_box.ends_visible(
            (maxcol, maxrow-head_rows) ):
            self.frame.footer = None
        else:
            self.frame.footer = self.footer

        return self.frame.render( (maxcol, maxrow), focus)

    def get_string_for_location(self, i):
        return f"{i:3} : {self._memory.get_as_string(i)}"

    def update(self):
        for i in range(len(self._memory)):
            self._memory_items[i].set_text(self.get_string_for_location(i))


    def keypress( self, size, key ):
        return self.list_box.keypress( size, key )