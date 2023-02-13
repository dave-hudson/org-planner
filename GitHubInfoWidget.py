from PySide6 import QtWidgets
from InfoWidget import InfoWidget

class GitHubInfoWidget(InfoWidget):
    """
    A widget class used to display information about grade structures.
    """
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._info_github_login = self._add_info_text("GitHub Login")
        self._info_github_profile_url = self._add_info_text("GitHub Profile URL")

    def update_contents(self):
        uen = self._uen

        p = self._people[uen]["Person"]

        github_login = "N/A"
        github_profile_url = "N/A"
        if "GitHub" in p.keys():
            github = p["GitHub"][-1]
            github_login = github["Login"]
            github_profile_url = github["Profile URL"]

        self._info_github_login.setText(github_login)
        self._info_github_profile_url.setText(github_profile_url)

    def set_locations(self, locations):
        pass

    def set_people(self, people, top_level_uen):
        self._people = people

    def set_uen(self, uen):
        self._uen = uen

    def set_zoom(self, zoom_factor):
        pass

    def set_redacted(self, is_redacted):
        pass
