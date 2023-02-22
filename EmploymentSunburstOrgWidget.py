from SunburstOrgWidget import SunburstOrgWidget

employment_colours = {}

class EmploymentSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw type sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        employment_type = p.get_employment()
        if employment_type in employment_colours:
            colours = employment_colours[employment_type]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = (
            f"{p.get_name()}"
            f"\nEmployment: {p.get_employment()}"
            f"\nFTE: {p.get_fte():.1f}"
        )

        return tt
