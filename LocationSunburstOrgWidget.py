from SunburstOrgWidget import SunburstOrgWidget

location_colours = {
    "UK": [0xff, 0x40, 0x33],
    "Ireland": [0x70, 0xe0, 0x2c],
    "India": [0xf0, 0xf0, 0x30],
    "Bulgaria": [0x40, 0xcc, 0xff],
    "Singapore": [0xff, 0x99, 0x33],
    "USA": [0xcc, 0x33, 0xff]
}

class LocationSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw location sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Locations" in p["Person"].keys():
            location = p["Person"]["Locations"][-1]["Location"]
            if location in location_colours:
                colours = location_colours[location]

        return colours
