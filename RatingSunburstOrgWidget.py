from SunburstOrgWidget import SunburstOrgWidget

rating_colours = {
    "1": [0x40, 0xa0, 0xff],
    "2": [0x40, 0xff, 0x40],
    "3": [0xff, 0xff, 0x40],
    "4": [0xff, 0xa0, 0x40],
    "5": [0xff, 0x40, 0x40]
}

class RatingSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw grade sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if "Ratings" in p.keys():
            rating = str(p["Ratings"][-1]["Rating"])
            if rating in rating_colours:
                colours = rating_colours[rating]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p["Name"]
        if "Ratings" in p.keys():
            tt += f"\nRating: {p['Ratings'][-1]['Rating']}"

        return tt
