from currencies import currencies, fx_rates
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalaryMidBandOffsetSunburstOrgWidget import (
    SalaryMidBandOffsetSunburstOrgWidget,
    salary_mid_band_offset_colours,
    salary_mid_band_offset_labels
)

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
        legend = ColourKey1DWidget(salary_mid_band_offset_colours, "Salary Offset Counts")
        legend.set_labels(salary_mid_band_offset_labels)
        self._org_widget = SunburstOrgKeyWidget(SalaryMidBandOffsetSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        salary = "N/A"
        salary_usd = ""
        salary_band_mid_point = "N/A"
        salary_band_mid_point_usd = ""
        salary_offset = "N/A"
        salary_offset_usd = ""
        if self._hide_sensitive_data:
            salary = "Hidden"
            salary_usd = ""
            salary_band_mid_point = "Hidden"
            salary_band_mid_point_usd = ""
            salary_offset = "Hidden"
            salary_offset_usd = ""
        else:
            p = self._people[uen]
            if "Salaries" in p.keys():
                location = p["Locations"][-1]["Location"]
                salary_val = p["Salaries"][-1]["Salary"]
                _, cur_sym = currencies[location]
                salary = f"{cur_sym}{salary_val:,}"
                salary_usd_val = salary_val * fx_rates[location]
                salary_usd = f" (${salary_usd_val:,.0f})"

            if "Salary Offset" in p.keys():
                location = p["Locations"][-1]["Location"]
                _, cur_sym = currencies[location]
                salary_band_mid_point = f"{cur_sym}{p['Salary Band Mid Point']:,.0f}"
                salary_band_mid_point_usd = f" (${p['Salary Band Mid Point USD']:,.0f})"
                salary_offset = (
                    f"{cur_sym}{p['Salary Offset']:,.0f}"
                    .replace(f"{cur_sym}-", f"-{cur_sym}")
                )
                salary_offset_usd = f" (${p['Salary Offset USD']:,.0f})".replace("$-", "-$")

        self._info_salary.setText(f"{salary} {salary_usd}")
        self._info_salary_band_mid_point.setText(
            f"{salary_band_mid_point} {salary_band_mid_point_usd}"
        )
        self._info_salary_offset.setText(f"{salary_offset} {salary_offset_usd}")
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
