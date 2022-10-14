import urwid

from slothpu import RegisterFile


class RegisterFileWidget(urwid.WidgetWrap):
    def __init__(self, register_file: RegisterFile):
        self._rf = register_file

        self._register_output = [urwid.Text("") for i in range(len(self._rf.registers))]
        self._A_text = urwid.Text("")
        self._B_text = urwid.Text("")
        self._C_text = urwid.Text("")

        all_text = [
            *self._register_output,
            urwid.Divider("-"),
            self._A_text,
            self._B_text,
            self._C_text,
        ]

        text_pile = urwid.Pile(all_text)

        reg_box = urwid.LineBox(
            text_pile, title="Register File", title_align=urwid.LEFT
        )
        self.update()
        super(RegisterFileWidget, self).__init__(reg_box)

    def update(self):
        for i in range(len(self._register_output)):
            self._register_output[i].set_text(self.format_register_string(i))
        self._A_text.set_text(self.format_regX_string("A", self._rf.A_register))
        self._B_text.set_text(self.format_regX_string("B", self._rf.B_register))
        self._C_text.set_text(
            self.format_regX_string("C", self._rf.C_register, self._rf.write_C_register)
        )

    def format_register_string(self, i: int) -> str:
        # Bits are stored little endian, so reverse for big endian
        return f"{i}: {self._rf.registers.get_as_string(i)}"

    def format_regX_string(
        self, reg_id: str, reg_idx: int, write_register: bool = False
    ):
        base_str = f"Register {reg_id}: {reg_idx}"
        if write_register:
            base_str = base_str + " (Write)"
        return base_str
