from PySide6 import QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from SalaryBandOffsetSunburstOrgWidget import SalaryBandOffsetSunburstOrgWidget, salary_band_offset_colours

class SalaryBandOffsetInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._is_manager = False
        self._hide_sensitive_data = True

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._info_salary_band_lower_limit = self._add_info_text("Salary Band Lower Limit")
        self._info_salary_band_salary = self._add_info_text("Salary")
        self._info_salary_band_upper_limit = self._add_info_text("Salary Band Upper Limit")
        self._info_salary_band_offset = self._add_info_text("Salary Comparison With Band")
        legend = ColourKey1DWidget(salary_band_offset_colours)
        self._org_widget = SunburstOrgKeyWidget(SalaryBandOffsetSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)

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

    def render_uen(self):
        uen = self._uen
        is_manager = self._is_manager
        p = self._people[uen]["Person"]

        salary_band_lower_limit = "N/A"
        salary_band_upper_limit = "N/A"
        salary_band_offset = "N/A"
        salary = "N/A"
        if self._hide_sensitive_data:
            salary_band_lower_limit = "Hidden"
            salary_band_upper_limit = "Hidden"
            salary_band_offset = "Hidden"
            salary = "Hidden"
        else:
            if "Salary Band Offset" in self._people[uen].keys():
                salary_band_lower_limit = self._people[uen]["Salary Band Lower Limit"]
                salary_band_upper_limit = self._people[uen]["Salary Band Upper Limit"]
                salary_band_offset = str(self._people[uen]["Salary Band Offset"])
                salary = str(p["Salaries"][-1]["Salary"])

        self._info_salary_band_lower_limit.setText(str(salary_band_lower_limit))
        self._info_salary_band_salary.setText(salary)
        self._info_salary_band_upper_limit.setText(str(salary_band_upper_limit))
        self._info_salary_band_offset.setText(salary_band_offset)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
