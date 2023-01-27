from SunburstOrgWidget import SunburstOrgWidget

class ServiceDurationSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw service duration sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        base_colour = int(0xe0 * p["Service Duration Fraction"])
        colours = [0xe0, 0xe0 - base_colour, 0xe0 - base_colour, 0xff]

        return colours