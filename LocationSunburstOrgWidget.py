from SunburstOrgWidget import SunburstOrgWidget

location_colours = {
    "UK": [0xff, 0x40, 0x33],
    "Ireland": [0x70, 0xe0, 0x2c],
    "India": [0xf0, 0xf0, 0x30],
    "Bulgaria": [0x40, 0xcc, 0xff],
    "Singapore": [0xff, 0x99, 0x33],
    "USA": [0xcc, 0x33, 0xff],
    "Brazil": [0x18, 0x3c, 0xb6],
    "Hong Kong": [0x40, 0x70, 0x2c],
    "Other": [0x60, 0x60, 0x60]
}

class LocationSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw location sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if "Locations" in p.keys():
            location = p["Locations"][-1]["Location"]
            if location in location_colours:
                colours = location_colours[location]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p["Name"]
        if "Locations" in p.keys():
            tt += f"\nLocation: {p['Locations'][-1]['Location']}"

        return tt
