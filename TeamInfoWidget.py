from InfoOrgKeyWidget import InfoOrgKeyWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from TeamColourKey1DWidget import TeamColourKey1DWidget
from TeamSunburstOrgWidget import TeamSunburstOrgWidget, team_colours

class TeamInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about team memberships.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_team = self._add_info_text("Team")
        legend = TeamColourKey1DWidget(team_colours)
        self._org_widget = SunburstOrgKeyWidget(TeamSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]
        self._info_team.setText(p["Teams"][-1]["Team"])
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
