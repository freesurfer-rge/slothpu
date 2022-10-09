import urwid

from slothpu import SlothPU

from ._instruction_register_widget import InstructionRegisterWidget
from ._program_counter_widget import ProgramCounterWidget
from ._status_register_widget import StatusRegisterWidget


class ControlColumn(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        self._spu = target

        pc_widget = ProgramCounterWidget(self._spu.program_counter)
        ir_widget = InstructionRegisterWidget(self._spu.instruction_register)
        sr_widget = StatusRegisterWidget(self._spu.status_register)

        control_pile = urwid.Pile(
            [
                urwid.Filler(pc_widget, valign=urwid.TOP),
                urwid.Filler(ir_widget, valign=urwid.TOP),
                urwid.Filler(sr_widget, valign=urwid.TOP)
            ]
        )

        self._widgets = [pc_widget, ir_widget, sr_widget]

        super(ControlColumn, self).__init__(control_pile)

    def update(self):
        for w in self._widgets:
            w.update()
