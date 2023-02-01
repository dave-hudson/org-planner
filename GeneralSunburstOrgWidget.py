from SunburstOrgWidget import SunburstOrgWidget

class GeneralSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw general sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

        self._ident_uen = 0

    def _get_brush_colour(self, uen):
        colours = [0x80, 0x80, 0x80]

        if uen == self._ident_uen:
            colours = [0xe0, 0x40, 0x40]

        return colours

    def set_ident_uen(self, ident_uen):
        self._ident_uen = ident_uen

        self.update()
