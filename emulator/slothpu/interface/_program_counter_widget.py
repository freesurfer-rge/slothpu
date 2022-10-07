import urwid

from slothpu import ProgramCounter


class ProgramCounterWidget(urwid.WidgetWrap):
    def __init__(self, pc: ProgramCounter):
        self._pc = pc

        self._pc_text = urwid.Text("")
        self._inc_enable_text = urwid.Text("")

        pc_pile = urwid.Pile([self._pc_text, self._inc_enable_text])

        pc_box = urwid.LineBox(
            
            pc_pile, title="Program Counter", title_align=urwid.LEFT
        )
        self.update()

        super(ProgramCounterWidget, self).__init__(pc_box)

    def update(self):
        self._pc_text.set_text(self._pc.get_as_string())
        self._inc_enable_text.set_text(f"Increment Enable: {self._pc.increment_enable}")
