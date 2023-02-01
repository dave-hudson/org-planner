from PySide6 import QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from GenderSunburstOrgWidget import GenderSunburstOrgWidget, gender_colours

class GenderInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._is_manager = False

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._info_gender = self._add_info_text("Gender")
        legend = ColourKey1DWidget(gender_colours, "Gender Counts")
        self._org_widget = SunburstOrgKeyWidget(GenderSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def set_locations(self, locations):
        self._org_widget.set_locations(locations)

    def set_people(self, people):
        self._people = people
        self._org_widget.set_people(people)

    def set_uen(self, uen):
        self._uen = uen

        is_manager = False
        if len(self._people[uen]["Direct Reports"]) != 0:
            is_manager = True

        self._is_manager = is_manager
        self._org_widget.set_uen(uen, is_manager)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]["Person"]

        gender = "None"
        if "Gender" in p.keys():
            gender = p["Gender"]

        self._info_gender.setText(gender)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
