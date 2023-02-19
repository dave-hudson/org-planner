from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from GenderSunburstOrgWidget import GenderSunburstOrgWidget, gender_colours

class GenderInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display gender information about a person.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_gender = self._add_info_text("Gender")
        legend = ColourKey1DWidget(gender_colours, "Gender Counts")
        self._org_widget = SunburstOrgKeyWidget(GenderSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]

        gender = "None"
        if "Gender" in p.keys():
            gender = p["Gender"]

        self._info_gender.setText(gender)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
