import urwid

from slothpu import SlothPU

from ._register_file_widget import RegisterFileWidget


class RegisterColumn(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        self._registers = RegisterFileWidget(target.register_file)

        # Have to use Filler or urwid gets unhappy
        register_pile = urwid.Pile(
            [
                urwid.Filler(self._registers, valign=urwid.TOP),
            ]
        )

        super(RegisterColumn, self).__init__(register_pile)

    def update(self):
        self._registers.update()
