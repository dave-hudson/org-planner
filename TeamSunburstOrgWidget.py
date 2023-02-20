from SunburstOrgWidget import SunburstOrgWidget

team_colours = {}

class TeamSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw team sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        team = p.get_team()
        if team in team_colours:
            colours = team_colours[team]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p.get_name()
        team = p.get_team()
        tt += f"\nTeam: {team}"

        return tt
