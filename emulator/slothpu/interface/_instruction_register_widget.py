import urwid

from slothpu import InstructionRegister


class InstructionRegisterWidget(urwid.WidgetWrap):
    def __init__(self, ir: InstructionRegister):
        self._ir = ir

        self._ir_text = urwid.Text(self._ir.get_as_string())
        self._unit_text = urwid.Text(f"Unit: {self._ir.unit}")
        self._R_A_text = urwid.Text(f"R_A : {self._ir.R_A}")
        self._R_B_text = urwid.Text(f"R_B : {self._ir.R_B}")
        self._R_C_text = urwid.Text(f"R_C : {self._ir.R_C}")

        ir_pile = urwid.Pile(
            [
                self._ir_text,
                self._unit_text,
                self._R_A_text,
                self._R_B_text,
                self._R_C_text,
            ]
        )

        ir_box = urwid.LineBox(
            ir_pile, title="Instruction Register", title_align=urwid.LEFT
        )

        super(InstructionRegisterWidget, self).__init__(ir_box)

    def update(self):
        self._ir_text.set_text(self._ir.get_as_string())
