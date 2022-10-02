import urwid

from slothpu import SlothPU


def top_handler(key):
    raise urwid.ExitMainLoop()


class PipelineStage(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        pipeline_txt = urwid.Text(target.pipeline_stage, align=urwid.LEFT, wrap=urwid.CLIP)
        box = urwid.LineBox(pipeline_txt, title="Current Pipeline Stage:", title_align=urwid.LEFT)
        super(PipelineStage, self).__init__(urwid.Filler(box, valign=urwid.MIDDLE))


class SlothPU_Interface:
    def __init__(self):
        self._target = SlothPU()

        self.top = PipelineStage(self._target)

    def main(self):
        urwid.MainLoop(self.top, unhandled_input=top_handler, input_filter=self.input_filter).run()

    def input_filter(self, input, raw_input):
        if 'q' in input or 'Q' in input:
            raise urwid.ExitMainLoop()

        # Prevent further processing of input
        return []


spu = SlothPU_Interface()
spu.main()
