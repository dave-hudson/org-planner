from SunburstOrgWidget import SunburstOrgWidget

type_colours = {}

class TypeSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw type sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Employment" in p["Person"]["Employments"][-1].keys():
            person_type = p["Person"]["Employments"][-1]["Employment"]
            if person_type in type_colours:
                colours = type_colours[person_type]

        return colours
