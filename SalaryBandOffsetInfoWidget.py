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
        salary_band = "N/A"
        salary_band_offset = "N/A"
        if self._hide_sensitive_data:
            salary = "Hidden"
            salary_band = "Hidden"
            salary_band_offset = "Hidden"
        else:
            p = self._people[uen]
            if p.has_salary_band():
                salary_str = p.get_salary_str()
                salary_usd_str = p.get_salary_usd_str()
                salary = f"{salary_str} ({salary_usd_str})"
                salary_band_lower_limit_str = p.get_salary_band_lower_limit_str()
                salary_band_upper_limit_str = p.get_salary_band_upper_limit_str()
                salary_band = f"{salary_band_lower_limit_str} to {salary_band_upper_limit_str}"
                salary_band_lower_limit_usd_str = p.get_salary_band_lower_limit_usd_str()
                salary_band_upper_limit_usd_str = p.get_salary_band_upper_limit_usd_str()
                salary_band += f" ({salary_band_lower_limit_usd_str} to {salary_band_upper_limit_usd_str})"
                salary_band_offset_str = p.get_salary_band_offset_str()
                salary_band_offset_usd_str = p.get_salary_band_offset_usd_str()
                salary_band_offset = f"{salary_band_offset_str} ({salary_band_offset_usd_str})"

        self._info_salary.setText(salary)
        self._info_salary_band.setText(salary_band)
        self._info_salary_band_offset.setText(salary_band_offset)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
