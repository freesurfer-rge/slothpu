import urwid

from slothpu import SlothPU

from ._output_registerfile_widget import OutputRegisterFileWidget
from ._backplane_widget import BackPlaneWidget
from ._memory_column import MemoryColumn
from ._pipeline_stage_widget import PipelineStageWidget


def top_handler(key):
    if "q" in key or "Q" in key:
        raise urwid.ExitMainLoop()


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


class SlothPU_Interface:
    def __init__(self):
        self._target = SlothPU()

        register_column = RegisterColumn(self._target)
        memory_column = MemoryColumn(self._target.main_memory)
        backplane = BackPlaneWidget(self._target.backplane)
        stage_bar = PipelineStageWidget(self)

        self._update_targets = [register_column, backplane, memory_column, stage_bar]

        self.top = urwid.Frame(
            header=stage_bar,
            body=urwid.Columns([register_column, memory_column], dividechars=1),
            footer=backplane,
            focus_part="body",
        )

    def update(self):
        for t in self._update_targets:
            t.update()

    def main(self):
        urwid.MainLoop(self.top, unhandled_input=top_handler).run()
