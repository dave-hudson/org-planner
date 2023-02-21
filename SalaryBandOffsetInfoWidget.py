from currencies import currencies
from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalaryBandOffsetColourKey1DWidget import SalaryBandOffsetColourKey1DWidget
from SalaryBandOffsetSunburstOrgWidget import (
    SalaryBandOffsetSunburstOrgWidget, salary_band_offset_colours, salary_band_offset_labels
)
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class SalaryBandOffsetInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about salary offsets from salary bands.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_salary = self._add_info_text("Salary")
        self._info_salary_band = self._add_info_text("Salary Band")
        self._info_salary_band_offset = self._add_info_text("Salary Band Offset")
        legend = SalaryBandOffsetColourKey1DWidget(salary_band_offset_colours)
        legend.set_labels(salary_band_offset_labels)
        self._org_widget = SunburstOrgKeyWidget(SalaryBandOffsetSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        salary = "N/A"
        salary_usd = ""
        salary_band = "N/A"
        salary_band_usd = ""
        salary_band_offset_str = "N/A"
        salary_band_offset_usd_str = ""
        if self._hide_sensitive_data:
            salary = "Hidden"
            salary_usd = ""
            salary_band = "Hidden"
            salary_band_usd = ""
            salary_band_offset_str = "Hidden"
            salary_band_offset_usd_str = ""
        else:
            p = self._people[uen]
            if p.has_salary_band():
                location = p.get_location()
                salary_val = p.get_salary()
                _, cur_sym = currencies[location]
                salary = f"{cur_sym}{salary_val:,}"
                salary_usd_val = p.get_salary_usd()
                salary_usd = f" (${salary_usd_val:,.0f})"

                salary_band_lower_limit = p.get_salary_band_lower_limit()
                salary_band_upper_limit = p.get_salary_band_upper_limit()
                salary_band = (
                    f"{cur_sym}{salary_band_lower_limit:,.0f} "
                    + f"to {cur_sym}{salary_band_upper_limit:,.0f}"
                )
                salary_band_lower_limit_usd = p.get_salary_band_lower_limit_usd()
                salary_band_upper_limit_usd = p.get_salary_band_upper_limit_usd()
                salary_band_usd = (
                    f" (${salary_band_lower_limit_usd:,.0f} to ${salary_band_upper_limit_usd:,.0f})"
                )
                salary_band_offset = p.get_salary_band_offset()
                salary_band_offset_str = (
                    f"{cur_sym}{salary_band_offset:,.0f}"
                    .replace(f"{cur_sym}-", f"-{cur_sym}")
                )
                salary_band_offset_usd = p.get_salary_band_offset_usd()
                salary_band_offset_usd_str = f" (${salary_band_offset_usd:,.0f})"

        self._info_salary.setText(f"{salary} {salary_usd}")
        self._info_salary_band.setText(f"{salary_band} {salary_band_usd}")
        self._info_salary_band_offset.setText(f"{salary_band_offset_str} {salary_band_offset_usd_str}")
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
