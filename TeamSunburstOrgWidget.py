from SunburstOrgWidget import SunburstOrgWidget

team_colours = {}

class TeamSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw team sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Team" in p["Person"].keys():
            team = p["Person"]["Team"]
            if team in team_colours:
                colours = team_colours[team]

        return colours
