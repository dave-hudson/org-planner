from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalaryColourKey1DWidget import SalaryColourKey1DWidget
from SalarySunburstOrgWidget import SalarySunburstOrgWidget, salary_colours
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class SalaryInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display salary information.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_salary = self._add_info_text("Salary")
        legend = SalaryColourKey1DWidget(salary_colours)
        self._org_widget = SunburstOrgKeyWidget(SalarySunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager
        p = self._people[uen]

        salary = "N/A"
        if self._hide_sensitive_data:
            salary = "Hidden"
        else:
            if p.has_salary():
                salary_str = p.get_salary_str()
                salary_usd_str = p.get_salary_usd_str()
                salary = f"{salary_str} ({salary_usd_str})"

        self._info_salary.setText(salary)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
