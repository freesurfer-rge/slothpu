import urwid

from slothpu import SlothPU


def top_handler(key):
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
        self._target = target

        self._registers = [
            urwid.Text(self.format_register_string(i))
            for i in reversed(range(self._target.n_registers))
        ]

        register_pile = urwid.Pile(self._registers)
        register_box = urwid.LineBox(
            register_pile, title="Registers", title_align=urwid.LEFT
        )

        super(RegisterColumn, self).__init__(
            urwid.Filler(register_box)
        )  # Have to use Filler or urwid gets unhappy

    def update(self):
        for i in range(self._target.n_registers):
            self._registers[i].set_text(
                self.format_register_string(self._target.n_registers - i - 1)
            )

    def format_register_string(self, i: int) -> str:
        return f"{i}: {self._target.get_register(i).to01()}"


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

        self.top = urwid.Columns(
            [StatusColumn(self._target), RegisterColumn(self._target)], dividechars=1
        )

    def main(self):
        urwid.MainLoop(
            self.top, unhandled_input=top_handler, input_filter=self.input_filter
        ).run()

    def input_filter(self, input, raw_input):
        if "q" in input or "Q" in input:
            raise urwid.ExitMainLoop()

        if " " in input:
            self._target.advance_pipeline()
            for w, _ in self.top.contents:
                w.update()

        # Prevent further processing of input
        return []
