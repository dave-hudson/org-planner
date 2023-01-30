from PySide6 import QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from SalaryBandOffsetSunburstOrgWidget import SalaryBandOffsetSunburstOrgWidget, salary_band_offset_colours, salary_band_offset_labels

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

        self._info_salary_band = self._add_info_text("Salary Band")
        self._info_salary_band_offset = self._add_info_text("Band Offset")
        self._info_salary_band_usd = self._add_info_text("Salary Band (USD)")
        self._info_salary_band_offset_usd = self._add_info_text("Band Offset (USD)")
        legend = ColourKey1DWidget(salary_band_offset_colours)
        legend.set_labels(salary_band_offset_labels)
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

        salary_band = "N/A"
        salary_band_offset = "N/A"
        salary_band_usd = "N/A"
        salary_band_offset_usd = "N/A"
        if self._hide_sensitive_data:
            salary_band = "Hidden"
            salary_band_offset = "Hidden"
            salary_band_usd = "Hidden"
            salary_band_offset_usd = "Hidden"
        else:
            if "Salary Band Offset" in self._people[uen].keys():
                salary_band_lower_limit = self._people[uen]["Salary Band Lower Limit"]
                salary_band_upper_limit = self._people[uen]["Salary Band Upper Limit"]
                salary_band = "{} to {}".format(salary_band_lower_limit, salary_band_upper_limit)
                salary_band_offset = str(self._people[uen]["Salary Band Offset"])
                salary_band_lower_limit_usd = self._people[uen]["Salary Band Lower Limit USD"]
                salary_band_upper_limit_usd = self._people[uen]["Salary Band Upper Limit USD"]
                salary_band_usd = "{} to {}".format(salary_band_lower_limit_usd, salary_band_upper_limit_usd)
                salary_band_offset_usd = str(self._people[uen]["Salary Band Offset USD"])

        self._info_salary_band.setText(str(salary_band))
        self._info_salary_band_offset.setText(salary_band_offset)
        self._info_salary_band_usd.setText(str(salary_band_usd))
        self._info_salary_band_offset_usd.setText(salary_band_offset_usd)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
