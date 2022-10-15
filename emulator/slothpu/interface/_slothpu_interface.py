from typing import List, Optional

import urwid

from slothpu import SlothPU

from ._backplane_widget import BackPlaneWidget
from ._memory_column import MemoryColumn
from ._pipeline_stage_widget import PipelineStageWidget
from ._control_column import ControlColumn
from ._register_column import RegisterColumn


def top_handler(key):
    if "q" in key or "Q" in key:
        raise urwid.ExitMainLoop()


class SlothPU_Interface:
    def __init__(self,initial_memory: Optional[List[int]] = None):
        self._target = SlothPU(initial_memory=initial_memory)

        control_column = ControlColumn(self._target)
        register_column = RegisterColumn(self._target)
        memory_column = MemoryColumn(self._target.main_memory)
        backplane = BackPlaneWidget(self._target.backplane)
        stage_bar = PipelineStageWidget(self)

        self._update_targets = [
            control_column,
            register_column,
            backplane,
            memory_column,
            stage_bar,
        ]

        self.top = urwid.Frame(
            header=stage_bar,
            body=urwid.Columns(
                [control_column, register_column, memory_column], dividechars=1
            ),
            footer=backplane,
            focus_part="body",
        )

    def update(self):
        for t in self._update_targets:
            t.update()

    def main(self):
        urwid.MainLoop(self.top, unhandled_input=top_handler).run()
