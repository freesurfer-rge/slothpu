import urwid

from slothpu import SlothPU


class PipelineStageWidget(urwid.WidgetWrap):
    def __init__(self, parent: "SlothPU_Interface"):
        self._spu = parent._target
        self._parent = parent
        self._curr_stage = urwid.Text(self._spu.pipeline_stage)
        self._advance_button = urwid.Button("Advance Pipeline", on_press=self.on_click)

        cs = urwid.Padding(self._curr_stage, align=urwid.LEFT)
        ab = urwid.Padding(self._advance_button, align=urwid.RIGHT)

        cols = urwid.Columns([cs, ab])

        super(PipelineStageWidget, self).__init__(cols)

    def on_click(self, choice):
        self._spu.advance_pipeline()
        self._parent.update()

    def update(self):
        self._curr_stage.set_text(self._spu.pipeline_stage)
