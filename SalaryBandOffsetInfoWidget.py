from currencies import currencies
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
            p = self._people[uen]
            if "Salary Band Offset" in p.keys():
                location = p["Person"]["Locations"][-1]["Location"]
                _, cur_sym = currencies[location]
                salary_band_lower_limit = p["Salary Band Lower Limit"]
                salary_band_upper_limit = p["Salary Band Upper Limit"]
                salary_band = (
                    f"{cur_sym}{salary_band_lower_limit:,.0f} "
                    + f"to {cur_sym}{salary_band_upper_limit:,.0f}"
                )
                salary_band_offset = (
                    f"{cur_sym}{p['Salary Band Offset']:,.0f}"
                    .replace(f"{cur_sym}-", f"-{cur_sym}")
                )
                salary_band_lower_limit_usd = p["Salary Band Lower Limit USD"]
                salary_band_upper_limit_usd = p["Salary Band Upper Limit USD"]
                salary_band_usd = (
                    f"${salary_band_lower_limit_usd:,.0f} to ${salary_band_upper_limit_usd:,.0f}"
                )
                salary_band_offset_usd = f"${p['Salary Band Offset USD']:,.0f}"

        self._info_salary_band.setText(salary_band)
        self._info_salary_band_offset.setText(salary_band_offset)
        self._info_salary_band_usd.setText(salary_band_usd)
        self._info_salary_band_offset_usd.setText(salary_band_offset_usd)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
