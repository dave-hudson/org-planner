from PySide6 import QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from SalaryOffsetSunburstOrgWidget import SalaryOffsetSunburstOrgWidget, salary_offset_colours, salary_offset_labels

class SalaryOffsetInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._is_manager = False
        self._hide_sensitive_data = True

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

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

    def set_locations(self, locations):
        self._org_widget.set_locations(locations)

    def set_people(self, people):
        self._people = people
        self._org_widget.set_people(people)

    def set_uen(self, uen):
        self._uen = uen

        is_manager = False
        if len(self._people[uen]["Direct Reports"]) != 0:
            is_manager = True

        self._is_manager = is_manager
        self._org_widget.set_uen(uen, is_manager)

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
            if "Salary Offset" in self._people[uen].keys():
                salary_offset_mid_point = str(self._people[uen]["Salary Band Mid Point"])
                salary_offset_mid_point_usd = str(self._people[uen]["Salary Band Mid Point USD"])
                salary_offset = str(self._people[uen]["Salary Offset"])
                salary_offset_usd = str(int(self._people[uen]["Salary Offset USD"]))
                salary_offset_percentage = "{:.1f}%".format(self._people[uen]["Salary Offset Percentage"])

        self._info_salary_offset_mid_point.setText(salary_offset_mid_point)
        self._info_salary_offset.setText(salary_offset)
        self._info_salary_offset_mid_point_usd.setText(salary_offset_mid_point_usd)
        self._info_salary_offset_usd.setText(salary_offset_usd)
        self._info_salary_offset_percentage.setText(salary_offset_percentage)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
