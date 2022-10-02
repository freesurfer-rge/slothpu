import urwid

from slothpu import RegisterFile

class OutputRegisterFileWidget(urwid.WidgetWrap):
    def __init__(self, registers: RegisterFile, name: str):
        self._title = name
        self._registerfile = registers

        self._register_output = [
            urwid.Text(self.format_register_string(i))
            for i in reversed(range(len(self._registerfile)))
        ]

        register_pile = urwid.Pile(self._register_output)
        register_box = urwid.LineBox(
            register_pile, title=self._title, title_align=urwid.LEFT
        )

        super(OutputRegisterFileWidget, self).__init__(
            register_box
        )

    def update(self):
        for i in range(len(self._registerfile)):
            self._register_output[i].set_text(
                self.format_register_string(len(self._registerfile) - i - 1)
            )

    
    def format_register_string(self, i: int) -> str:
        # Bits are stored little endian, so reverse for big endian
        return f"{i}: {self._registerfile.get_as_string(i)}"