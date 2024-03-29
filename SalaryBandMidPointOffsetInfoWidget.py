from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalaryBandMidPointOffsetColourKey1DWidget import SalaryBandMidPointOffsetColourKey1DWidget
from SalaryBandMidPointOffsetSunburstOrgWidget import (
    SalaryBandMidPointOffsetSunburstOrgWidget,
    salary_band_mid_point_offset_colours,
    salary_band_mid_point_offset_labels
)
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class SalaryBandMidPointOffsetInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about offsets of salaries from
    salary band mid-points.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_salary = self._add_info_text("Salary")
        self._info_salary_band_mid_point = self._add_info_text("Salary Band Mid Point")
        self._info_salary_band_mid_point_offset = self._add_info_text(
            "Salary Band Mid Point Offset"
        )
        legend = SalaryBandMidPointOffsetColourKey1DWidget(salary_band_mid_point_offset_colours)
        legend.set_labels(salary_band_mid_point_offset_labels)
        self._org_widget = SunburstOrgKeyWidget(
            SalaryBandMidPointOffsetSunburstOrgWidget(), legend
        )
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        salary = "N/A"
        salary_band_mid_point = "N/A"
        salary_band_mid_point_offset = "N/A"
        if self._hide_sensitive_data:
            salary = "Hidden"
            salary_band_mid_point = "Hidden"
            salary_band_mid_point_offset = "Hidden"
        else:
            p = self._people[uen]
            if p.has_salary_band():
                salary = f"{p.get_salary_str()} ({p.get_salary_usd_str()})"
                salary_band_mid_point = (
                    f"{p.get_salary_band_mid_point_str()} "
                    f"({p.get_salary_band_mid_point_usd_str()})"
                )
                salary_band_mid_point_offset = (
                    f"{p.get_salary_band_mid_point_offset_str()} "
                    f"({p.get_salary_band_mid_point_offset_usd_str()})"
                )

        self._info_salary.setText(salary)
        self._info_salary_band_mid_point.setText(salary_band_mid_point)
        self._info_salary_band_mid_point_offset.setText(salary_band_mid_point_offset)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
