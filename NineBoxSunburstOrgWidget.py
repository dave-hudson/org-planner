from SunburstOrgWidget import SunburstOrgWidget

nine_box_colours = {
    "High": {
        "Low": [0xff, 0xff, 0x40],
        "Medium": [0xa0, 0xff, 0xa0],
        "High": [0x40, 0xff, 0xff]
    },
    "Medium": {
        "Low": [0xff, 0xa0, 0x40],
        "Medium": [0xa0, 0xa0, 0xa0],
        "High": [0x40, 0xa0, 0xff]
    },
    "Low": {
        "Low": [0xff, 0x40, 0x40],
        "Medium": [0xa0, 0x40, 0xa0],
        "High": [0x40, 0x40, 0xff]
    }
}

class NineBoxSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw nine-box grid sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if p.has_nine_box():
            nine_box_potential = p.get_nine_box_potential()
            nine_box_performance = p.get_nine_box_performance()
            if nine_box_potential in nine_box_colours:
                potential_colours = nine_box_colours[nine_box_potential]
                if nine_box_performance in potential_colours:
                    colours = potential_colours[nine_box_performance]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p.get_name()
        if p.has_nine_box():
            nine_box_potential = p.get_nine_box_potential()
            nine_box_performance = p.get_nine_box_performance()
            tt += f"\nPotential: {nine_box_potential}"
            tt += f"\nPerformance: {nine_box_performance}"

        return tt
