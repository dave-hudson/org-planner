from PySide6 import QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from NumDirectReportsSunburstOrgWidget import NumDirectReportsSunburstOrgWidget, num_direct_reports_colours

class NumDirectReportsInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._is_manager = False

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._info_num_direct_reports = self._add_info_text("Direct Reports")
        self._info_total_reports = self._add_info_text("Total Reports")
        legend = ColourKey1DWidget(num_direct_reports_colours, "Num Direct Reports Counts")
        self._org_widget = SunburstOrgKeyWidget(NumDirectReportsSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)

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

    def render_uen(self):
        uen = self._uen
        is_manager = self._is_manager

        self._info_num_direct_reports.setText(str(self._people[uen]["Num Direct Reports"]))
        self._info_total_reports.setText(str(self._people[uen]["Total Reports"]))
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass