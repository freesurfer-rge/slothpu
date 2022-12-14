import urwid

from slothpu import SlothPU


class PipelineStageWidget(urwid.WidgetWrap):
    def __init__(self, parent):
        self._spu: SlothPU = parent._target
        self._parent = parent
        self._curr_stage = urwid.Text("")
        self._advance_pipeline_button = urwid.Button(
            "Advance Pipeline", on_press=self.on_click_advance_stage
        )
        self._advance_instruction_button = urwid.Button(
            "Advance Instruction", on_press=self.on_click_advance_instruction
        )

        cs = urwid.AttrMap(
            urwid.Padding(self._curr_stage, align=urwid.LEFT), attr_map="stage_palette"
        )
        apb = urwid.AttrMap(
            urwid.Padding(self._advance_pipeline_button, align=urwid.RIGHT),
            attr_map="button_palette",
        )
        aib = urwid.AttrMap(
            urwid.Padding(self._advance_instruction_button, align=urwid.LEFT),
            attr_map="button_palette",
        )

        cols = urwid.Columns([cs, apb, aib], dividechars=2)
        self.update()
        super(PipelineStageWidget, self).__init__(cols)

    def on_click_advance_stage(self, choice):
        self._spu.advance_pipeline()
        self._parent.update()

    def on_click_advance_instruction(self, choice):
        self._spu.advance_instruction()
        self._parent.update()

    def update(self):
        self._curr_stage.set_text(self._spu.pipeline_stage)
