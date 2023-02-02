from PySide6 import QtWidgets, QtCore
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from TeamSunburstOrgWidget import TeamSunburstOrgWidget, team_colours

class TeamInfoWidget(InfoOrgKeyWidget):
    def __init__(self) -> None:
        super().__init__()

        self._info_team = self._add_info_text("Team")
        legend = ColourKey1DWidget(team_colours, "Team Counts")
        self._org_widget = SunburstOrgKeyWidget(TeamSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]["Person"]
        self._info_team.setText(p["Team"])
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
