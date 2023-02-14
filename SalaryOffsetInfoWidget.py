from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from SunburstOrgWidget import currencies
from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalaryOffsetSunburstOrgWidget import (
    SalaryOffsetSunburstOrgWidget, salary_offset_colours, salary_offset_labels
)

class SalaryOffsetInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about offsets of salaries from
    salary band mid-points.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_salary_offset_mid_point = self._add_info_text("Mid-band Salary")
        self._info_salary_offset = self._add_info_text("Mid-band Salary Offset")
        self._info_salary_offset_mid_point_usd = self._add_info_text("Mid-band Salary (USD)")
        self._info_salary_offset_usd = self._add_info_text("Mid-band Salary Offset (USD)")
        self._info_salary_offset_percentage = self._add_info_text("Mid-band Salary Offset (%)")
        legend = ColourKey1DWidget(salary_offset_colours, "Salary Offset Counts")
        legend.set_labels(salary_offset_labels)
        self._org_widget = SunburstOrgKeyWidget(SalaryOffsetSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        salary_offset_mid_point = "N/A"
        salary_offset_mid_point_usd = "N/A"
        salary_offset = "N/A"
        salary_offset_usd = "N/A"
        salary_offset_percentage = "N/A"
        if self._hide_sensitive_data:
            salary_offset_mid_point = "Hidden"
            salary_offset_mid_point_usd = "Hidden"
            salary_offset = "Hidden"
            salary_offset_usd = "Hidden"
            salary_offset_percentage = "Hidden"
        else:
            p = self._people[uen]
            if "Salary Offset" in p.keys():
                location = p["Person"]["Locations"][-1]["Location"]
                _, cur_sym = currencies[location]
                salary_offset_mid_point = f"{cur_sym}{p['Salary Band Mid Point']:,}"
                salary_offset_mid_point_usd = f"${p['Salary Band Mid Point USD']:,}"
                salary_offset = (
                    f"{cur_sym}{p['Salary Offset']:,}"
                    .replace(f"{cur_sym}-", f"-{cur_sym}")
                )
                salary_offset_usd = f"${p['Salary Offset USD']:,.0f}".replace("$-", "-$")
                salary_offset_percentage = f"{p['Salary Offset Percentage']:.1f}%"

        self._info_salary_offset_mid_point.setText(salary_offset_mid_point)
        self._info_salary_offset.setText(salary_offset)
        self._info_salary_offset_mid_point_usd.setText(salary_offset_mid_point_usd)
        self._info_salary_offset_usd.setText(salary_offset_usd)
        self._info_salary_offset_percentage.setText(salary_offset_percentage)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
