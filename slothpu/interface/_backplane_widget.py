import urwid

from slothpu import BackPlane

from ._bus_widget import BusWidget


class BackPlaneWidget(urwid.WidgetWrap):
    def __init__(self, backplane: BackPlane):
        self._backplane = backplane

        self._bus_widgets = [
            BusWidget(self._backplane.A_bus, "A"),
            BusWidget(self._backplane.B_bus, "B"),
            BusWidget(self._backplane.W_bus, "W"),
        ]

        bus_pile = urwid.Pile(self._bus_widgets)

        bp_box = urwid.LineBox(
            urwid.Padding(bus_pile, align=urwid.CENTER),
            title="BackPlane",
            title_align=urwid.LEFT,
        )

        super(BackPlaneWidget, self).__init__(bp_box)

    def update(self):
        for bw in self._bus_widgets:
            bw.update()