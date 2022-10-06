import urwid

from slothpu import InstructionRegister


class InstructionRegisterWidget(urwid.WidgetWrap):
    def __init__(self, ir: InstructionRegister):
        self._ir = ir

        self._ir_text = urwid.Text(self._ir.get_as_string())

        ir_box = urwid.LineBox(
            self._ir_text, title="Instruction Register", title_align=urwid.LEFT
        )

        super(InstructionRegisterWidget, self).__init__(ir_box)

    def update(self):
        self._ir_text.set_text(self._ir.get_as_string())
