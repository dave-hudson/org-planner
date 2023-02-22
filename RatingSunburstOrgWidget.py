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
        if p.has_rating():
            rating = str(p.get_rating())
            if rating in rating_colours:
                colours = rating_colours[rating]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p.get_name()
        if p.has_rating():
            tt += f"\nRating: {str(p.get_rating())}"

        return tt
