import urwid

from slothpu import Bus


class BusWidget(urwid.WidgetWrap):
    def __init__(self, bus: Bus, name: str):
        self._title = name
        self._bus = bus

        self._bus_text = urwid.Text(self.get_output_string())
        super(BusWidget, self).__init__(self._bus_text)

    def update(self):
        self._bus_text.set_text(self.get_output_string())

    def get_output_string(self):
        return f"{self._title} : {self._bus.to01()}"
