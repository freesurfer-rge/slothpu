import urwid


class FlagWidget(urwid.WidgetWrap):
    def __init__(self, name: str, value: int):
        self._name = name

        self._txt = urwid.Text(self.get_string(value))

        super(FlagWidget, self).__init__(self._txt)

    def get_string(self, value: int) -> str:
        return f"{self._name} : {value}"

    def update(self, value: int):
        self._txt.set_text(self.get_string(value))
