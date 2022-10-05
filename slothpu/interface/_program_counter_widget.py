import urwid

from slothpu import ProgramCounter

class ProgramCounterWidget(urwid.WidgetWrap):
    def __init__(self, pc: ProgramCounter):
        self._pc = pc

        self._pc_text = urwid.Text(self._pc.get_as_string())

        pc_box =    urwid.LineBox(
            self._pc_text, title="Program Counter", title_align=urwid.LEFT
        )

        super(ProgramCounter, self).__init__(pc_box)

    def update(self):
        self._pc_text.set_text(self._pc.get_as_string())