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
        self._info_percentage_time = self._add_info_text("FTE (%)")
        legend = EmploymentColourKey1DWidget(employment_colours)
        self._org_widget = SunburstOrgKeyWidget(EmploymentSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        e = self._people[uen]["Employments"][-1]
        self._info_type.setText(e["Employment"])
        self._org_widget.set_uen(uen, is_manager)

        percentage_time = 100
        if "Percentage Time" in e.keys():
            percentage_time = e["Percentage Time"]

        self._info_percentage_time.setText(f"{percentage_time}%")

    def set_redacted(self, is_redacted):
        pass
