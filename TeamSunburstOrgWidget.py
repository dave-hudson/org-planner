from SunburstOrgWidget import SunburstOrgWidget

team_colours = {}

class TeamSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw team sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if "Teams" in p.keys():
            team = p["Teams"][-1]["Team"]
            if team in team_colours:
                colours = team_colours[team]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p["Name"]
        if "Teams" in p.keys():
            tt += f"\nTeam: {p['Teams'][-1]['Team']}"

        return tt
