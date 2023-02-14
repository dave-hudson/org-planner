from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalaryBandOffsetSunburstOrgWidget import (
    SalaryBandOffsetSunburstOrgWidget, salary_band_offset_colours, salary_band_offset_labels
)

class SalaryBandOffsetInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about salary offsets from salary bands.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_salary_band = self._add_info_text("Salary Band")
        self._info_salary_band_offset = self._add_info_text("Band Offset")
        self._info_salary_band_usd = self._add_info_text("Salary Band (USD)")
        self._info_salary_band_offset_usd = self._add_info_text("Band Offset (USD)")
        legend = ColourKey1DWidget(salary_band_offset_colours, "Salary Band Offset Counts")
        legend.set_labels(salary_band_offset_labels)
        self._org_widget = SunburstOrgKeyWidget(SalaryBandOffsetSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
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
                salary_band = f"{salary_band_lower_limit:,} to {salary_band_upper_limit:,}"
                salary_band_offset = f"{self._people[uen]['Salary Band Offset']:,}"
                salary_band_lower_limit_usd = self._people[uen]["Salary Band Lower Limit USD"]
                salary_band_upper_limit_usd = self._people[uen]["Salary Band Upper Limit USD"]
                salary_band_usd = f"{salary_band_lower_limit_usd:,} to {salary_band_upper_limit_usd:,}"
                salary_band_offset_usd = f"{self._people[uen]['Salary Band Offset USD']:,}"

        self._info_salary_band.setText(salary_band)
        self._info_salary_band_offset.setText(salary_band_offset)
        self._info_salary_band_usd.setText(salary_band_usd)
        self._info_salary_band_offset_usd.setText(salary_band_offset_usd)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
