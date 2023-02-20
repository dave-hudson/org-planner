from InfoOrgKeyWidget import InfoOrgKeyWidget
from NumDirectReportsColourKey1DWidget import NumDirectReportsColourKey1DWidget
from NumDirectReportsSunburstOrgWidget import (
    NumDirectReportsSunburstOrgWidget, num_direct_reports_colours
)
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class NumDirectReportsInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about numbers of direct reports.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_num_direct_reports = self._add_info_text("Direct Reports")
        self._info_total_reports = self._add_info_text("Total Reports")
        legend = NumDirectReportsColourKey1DWidget(num_direct_reports_colours)
        self._org_widget = SunburstOrgKeyWidget(NumDirectReportsSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        self._info_num_direct_reports.setText(str(self._people[uen]["Num Direct Reports"]))
        self._info_total_reports.setText(str(self._people[uen]["Total Reports"]))
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
