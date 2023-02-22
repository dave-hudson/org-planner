from EmploymentColourKey1DWidget import EmploymentColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from EmploymentSunburstOrgWidget import EmploymentSunburstOrgWidget, employment_colours

class EmploymentInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about employee type.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_type = self._add_info_text("Employment")
        self._info_fte = self._add_info_text("FTE")
        legend = EmploymentColourKey1DWidget(employment_colours)
        self._org_widget = SunburstOrgKeyWidget(EmploymentSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]
        self._info_type.setText(p.get_employment())
        self._org_widget.set_uen(uen, is_manager)

        self._info_fte.setText(f"{p.get_fte():.1f}")

    def set_redacted(self, is_redacted):
        pass
