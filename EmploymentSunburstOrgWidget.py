from SunburstOrgWidget import SunburstOrgWidget

employment_colours = {}

class EmploymentSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw type sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Employment" in p["Person"]["Employments"][-1].keys():
            employment_type = p["Person"]["Employments"][-1]["Employment"]
            if employment_type in employment_colours:
                colours = employment_colours[employment_type]

        return colours
