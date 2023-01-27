from SunburstOrgWidget import SunburstOrgWidget

type_colours = {}

class TypeSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw type sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Type" in p["Person"].keys():
            type = p["Person"]["Type"]
            if type in type_colours:
                colours = type_colours[type]

        return colours
