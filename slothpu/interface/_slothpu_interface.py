import urwid

from slothpu import SlothPU

from ._output_registerfile_widget import OutputRegisterFileWidget
from ._backplane_widget import BackPlaneWidget
from ._memory_column import MemoryColumn


def top_handler(key):
    if "q" in key or "Q" in key:
        raise urwid.ExitMainLoop()


class StatusColumn(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        self._target = target
        self._pipeline_stage = PipelineStage(self._target)

        contents = urwid.Pile([self._pipeline_stage])

        super(StatusColumn, self).__init__(contents)

    def update(self):
        self._pipeline_stage.update()


class RegisterColumn(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        self._registers = OutputRegisterFileWidget(target.registers, "Registers")
        self._output_registers = OutputRegisterFileWidget(
            target.output_registers, "Output Registers"
        )

        # Have to use Filler or urwid gets unhappy
        register_pile = urwid.Pile(
            [urwid.Filler(self._registers), urwid.Filler(self._output_registers)]
        )

        super(RegisterColumn, self).__init__(register_pile)

    def update(self):
        self._registers.update()


class PipelineStage(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        self._target = target
        self._pipeline_txt = urwid.Text(
            self._target.pipeline_stage, align=urwid.LEFT, wrap=urwid.CLIP
        )
        box = urwid.LineBox(
            self._pipeline_txt, title="Current Pipeline Stage:", title_align=urwid.LEFT
        )
        super(PipelineStage, self).__init__(urwid.Filler(box, valign=urwid.MIDDLE))

    def update(self):
        self._pipeline_txt.set_text(self._target.pipeline_stage)


class SlothPU_Interface:
    def __init__(self):
        self._target = SlothPU()

        status_column = StatusColumn(self._target)
        register_column = RegisterColumn(self._target)
        memory_column = MemoryColumn(self._target.memory)
        backplane = BackPlaneWidget(self._target.backplane)

        self._update_targets = [
            status_column,
            register_column,
            backplane,
            memory_column,
        ]

        self.top = urwid.Pile(
            [
                urwid.Columns(
                    [status_column, register_column, memory_column], dividechars=1
                ),
                urwid.Filler(backplane, valign=urwid.MIDDLE),
            ]
        )

    def main(self):
        urwid.MainLoop(self.top, unhandled_input=top_handler).run()
