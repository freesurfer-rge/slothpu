import urwid

from slothpu import InstructionRegister


class InstructionRegisterWidget(urwid.WidgetWrap):
    def __init__(self, ir: InstructionRegister):
        self._ir = ir

        self._ir_text = urwid.Text(self._ir.get_as_string())
        self._unit_text = urwid.Text(self._get_unit_string())
        self._operation_text = urwid.Text(self._get_operation_string())
        self._ct_text = urwid.Text(self._get_ct_string())

        ir_pile = urwid.Pile(
            [
                self._ir_text,
                self._unit_text,
                self._operation_text,
                self._ct_text,
            ]
        )

        ir_box = urwid.LineBox(
            ir_pile, title="Instruction Register", title_align=urwid.LEFT
        )

        super(InstructionRegisterWidget, self).__init__(ir_box)

    def update(self):
        self._ir_text.set_text(self._ir.get_as_string())
        self._unit_text.set_text(self._get_unit_string())
        self._operation_text.set_text(self._get_operation_string())
        self._ct_text.set_text(self._get_ct_string())

    def _get_unit_string(self) -> str:
        return f"Unit     : {self._ir.unit}"

    def _get_operation_string(self) -> str:
        return f"Operation: {self._ir.operation}"

    def _get_ct_string(self) -> str:
        return f"Target   : {self._ir.commit_target}"
