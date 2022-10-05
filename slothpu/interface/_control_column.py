import urwid

from slothpu import SlothPU

from ._program_counter_widget import ProgramCounterWidget


class ControlColumn(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        self._spu = target

        self._pc_widget = ProgramCounterWidget(self._spu.program_counter)

        control_pile = urwid.Pile([urwid.Filler(self._pc_widget, valign=urwid.TOP)])

        super(ControlColumn, self).__init__(control_pile)

    def update(self):
        self._pc_widget.update()
