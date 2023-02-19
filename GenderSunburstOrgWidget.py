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
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if "Gender" in p.keys():
            gender = p["Gender"]
            if gender in gender_colours:
                colours = gender_colours[gender]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p["Name"]
        if "Gender" in p.keys():
            tt += f"\nGender: {p['Gender']}"

        return tt
