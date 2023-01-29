from SunburstOrgWidget import SunburstOrgWidget

gender_colours = {
    "M": [0x40, 0xc0, 0xff],
    "F": [0xff, 0x80, 0x80],
    "NB": [0xf0, 0xf0, 0x30]
}

class GenderSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw gender sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Gender" in p["Person"].keys():
            gender = p["Person"]["Gender"]
            if gender in gender_colours:
                colours = gender_colours[gender]

        return colours
