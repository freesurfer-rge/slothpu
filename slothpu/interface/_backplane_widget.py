import urwid

from slothpu import BackPlane

from ._bus_widget import BusWidget
from ._flag_widget import FlagWidget


class BackPlaneWidget(urwid.WidgetWrap):
    def __init__(self, backplane: BackPlane):
        self._backplane = backplane

        self._bus_widgets = [
            BusWidget(self._backplane.A_bus, "A"),
            BusWidget(self._backplane.B_bus, "B"),
            BusWidget(self._backplane.W_bus, "W"),
        ]

        self._salu_widget = FlagWidget("SALU Flag", self._backplane.SALU_flag)
        self._dalu_widget = FlagWidget("DALU Flag", self._backplane.DALU_flag)

        bp_pile = urwid.Pile(self._bus_widgets)
        flag_pile = urwid.Pile([self._salu_widget, self._dalu_widget])

        bp_box = urwid.LineBox(
            urwid.Columns([bp_pile, flag_pile], dividechars=4),
            title="BackPlane",
            title_align=urwid.LEFT,
        )

        super(BackPlaneWidget, self).__init__(bp_box)

    def update(self):
        for bw in self._bus_widgets:
            bw.update()
        self._salu_widget.update(self._backplane.SALU_flag)
        self._dalu_widget.update(self._backplane.DALU_flag)
