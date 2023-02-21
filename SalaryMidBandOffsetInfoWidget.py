from currencies import currencies, fx_rates
from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalaryMidBandOffsetColourKey1DWidget import SalaryMidBandOffsetColourKey1DWidget
from SalaryMidBandOffsetSunburstOrgWidget import (
    SalaryMidBandOffsetSunburstOrgWidget,
    salary_mid_band_offset_colours,
    salary_mid_band_offset_labels
)
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class SalaryMidBandOffsetInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about offsets of salaries from
    salary band mid-points.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_salary = self._add_info_text("Salary")
        self._info_salary_band_mid_point = self._add_info_text("Salary Mid-band")
        self._info_salary_offset = self._add_info_text("Salary Mid-band Offset")
        legend = SalaryMidBandOffsetColourKey1DWidget(salary_mid_band_offset_colours)
        legend.set_labels(salary_mid_band_offset_labels)
        self._org_widget = SunburstOrgKeyWidget(SalaryMidBandOffsetSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        salary = "N/A"
        salary_usd = ""
        salary_band_mid_point_str = "N/A"
        salary_band_mid_point_usd_str = ""
        salary_offset_str = "N/A"
        salary_offset_usd_str = ""
        if self._hide_sensitive_data:
            salary = "Hidden"
            salary_usd = ""
            salary_band_mid_point_str = "Hidden"
            salary_band_mid_point_usd_str = ""
            salary_offset_str = "Hidden"
            salary_offset_usd_str = ""
        else:
            p = self._people[uen]
            if p.has_salary_band():
                location = p.get_location()
                salary_val = p.get_salary()
                _, cur_sym = currencies[location]
                salary = f"{cur_sym}{salary_val:,}"
                salary_usd_val = salary_val * fx_rates[location]
                salary_usd = f" (${salary_usd_val:,.0f})"

                salary_band_mid_point = p.get_salary_band_mid_point()
                salary_band_mid_point_str = f"{cur_sym}{salary_band_mid_point:,.0f}"
                salary_band_mid_point_usd = p.get_salary_band_mid_point_usd()
                salary_band_mid_point_usd_str = f" (${salary_band_mid_point_usd:,.0f})"
                salary_offset = p.get_salary_offset()
                salary_offset_str = (
                    f"{cur_sym}{salary_offset:,.0f}"
                    .replace(f"{cur_sym}-", f"-{cur_sym}")
                )
                salary_offset_usd = p.get_salary_mid_band_offset_usd()
                salary_offset_usd_str = f" (${salary_offset_usd:,.0f})".replace("$-", "-$")

        self._info_salary.setText(f"{salary} {salary_usd}")
        self._info_salary_band_mid_point.setText(
            f"{salary_band_mid_point_str} {salary_band_mid_point_usd_str}"
        )
        self._info_salary_offset.setText(f"{salary_offset_str} {salary_offset_usd_str}")
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
