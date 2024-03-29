from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from RollupSalarySunburstOrgWidget import RollupSalarySunburstOrgWidget, rollup_salary_colours

class RollupSalaryInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display roll-up salary information.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_rollup_salary_usd = self._add_info_text("Rollup Salaries")
        legend = ColourKey1DWidget(rollup_salary_colours)
        self._org_widget = SunburstOrgKeyWidget(RollupSalarySunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        rollup_salary_usd = "N/A"
        if self._hide_sensitive_data:
            rollup_salary_usd = "Hidden"
        else:
            p = self._people[uen]
            (rollup_salaries, missing_salaries) = p.get_rollup_salaries(self._people)
            rollup_salary_usd = f"${rollup_salaries:,.0f}"

            if missing_salaries > 0:
                ppl = "People"
                if missing_salaries == 1:
                    ppl = "Person"

                rollup_salary_usd += f" (Missing {missing_salaries:d} {ppl})"

        self._info_rollup_salary_usd.setText(rollup_salary_usd)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
