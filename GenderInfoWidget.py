from GenderColourKey1DWidget import GenderColourKey1DWidget
from GenderSunburstOrgWidget import GenderSunburstOrgWidget, gender_colours
from InfoOrgKeyWidget import InfoOrgKeyWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class GenderInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display gender information about a person.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_gender = self._add_info_text("Gender")
        legend = GenderColourKey1DWidget(gender_colours)
        self._org_widget = SunburstOrgKeyWidget(GenderSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]
        gender = p.get_gender()

        self._info_gender.setText(gender)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
