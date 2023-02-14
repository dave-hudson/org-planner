from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgWidget import fx_rates
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from SalarySunburstOrgWidget import SalarySunburstOrgWidget, salary_colours

class SalaryInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display salary information.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_salary = self._add_info_text("Salary")
        self._info_salary_usd = self._add_info_text("Salary (USD)")
        legend = ColourKey1DWidget(salary_colours, "Salary Counts")
        self._org_widget = SunburstOrgKeyWidget(SalarySunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager
        p = self._people[uen]["Person"]

        salary = "N/A"
        salary_usd = "N/A"
        if self._hide_sensitive_data:
            salary = "Hidden"
            salary_usd = "Hidden"
        else:
            if "Salaries" in p.keys():
                salary_val = p["Salaries"][-1]["Salary"]
                salary = f"{salary_val:,}"
                salary_usd_val = salary_val * fx_rates[p["Locations"][-1]["Location"]]
                salary_usd = f"{salary_usd_val:,.0f}"

        self._info_salary.setText(salary)
        self._info_salary_usd.setText(salary_usd)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
