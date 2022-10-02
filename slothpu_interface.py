import urwid

from slothpu import SlothPU

def top_handler(key):
    raise urwid.ExitMainLoop()

class PipelineStage(urwid.WidgetWrap):
    def __init__(self, target: SlothPU):
        txt = urwid.Text(target.pipeline_stage, align=urwid.CENTER, wrap=urwid.CLIP)
        super(PipelineStage, self).__init__(
            urwid.Filler(txt, valign=urwid.MIDDLE)
        )


class SlothPU_Interface:
    def __init__(self):
        self._target = SlothPU()

        self.top = PipelineStage(self._target)

spu = SlothPU_Interface()
urwid.MainLoop(spu.top, unhandled_input=top_handler).run()