from SunburstOrgWidget import SunburstOrgWidget

grade_colours = {
    "A": [0xdb, 0x1f, 0x00],
    "B": [0xf5, 0x78, 0x04],
    "C.H": [0xf8, 0xc7, 0x10],
    "C": [0xfb, 0xeb, 0x17],
    "C.L": [0xfd, 0xfa, 0x19],
    "D.H": [0x90, 0xc6, 0x12],
    "D": [0x60, 0xb8, 0x10],
    "D.L": [0x38, 0xaa, 0x0e],
    "E.H": [0x33, 0x9e, 0xc5],
    "E": [0x28, 0x7e, 0xbb],
    "E.L": [0x1e, 0x60, 0xb4],
    "F": [0x63, 0x40, 0xb5],
    "G": [0xa9, 0x2c, 0xb6]
}

class GradeSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw grade sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]["Person"]
        if "Grades" in p.keys():
            grade = p["Grades"][-1]["Grade"]
            if grade in grade_colours:
                colours = grade_colours[grade]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]["Person"]
        tt = p["Name"]
        if "Grades" in p.keys():
            tt += f"\nGrade: {p['Grades'][-1]['Grade']}"

        return tt
