import urwid

from slothpu import StatusRegister


class StatusRegisterWidget(urwid.WidgetWrap):
    def __init__(self, status_register: StatusRegister):
        self._sr = status_register

        self._sr_text = urwid.Text("")
        self._salu_text = urwid.Text("")
        self._dalu_text = urwid.Text("")

        status_pile = urwid.Pile([self._sr_text, self._salu_text, self._dalu_text])

        sr_box = urwid.LineBox(
            status_pile, title="Status Register", title_align=urwid.LEFT
        )
        self.update()

        super(StatusRegisterWidget, self).__init__(sr_box)

    def update(self):
        self._sr_text.set_text(f"Status: {self._sr.get_as_string()}")
        self._salu_text.set_text(
            f"SALU: {self._sr.value[StatusRegister.salu_bit] == 1}"
        )
        self._dalu_text.set_text(
            f"DALU: {self._sr.value[StatusRegister.dalu_bit] == 1}"
        )
