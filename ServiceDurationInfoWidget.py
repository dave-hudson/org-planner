from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from ServiceDurationSunburstOrgWidget import (
    ServiceDurationSunburstOrgWidget, service_duration_colours
)

class ServiceDurationInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about length of service.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_start_date = self._add_info_text("Start Date")
        self._info_service_duration = self._add_info_text("Service Duration")
        legend = ColourKey1DWidget(service_duration_colours)
        self._org_widget = SunburstOrgKeyWidget(ServiceDurationSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]

        self._info_start_date.setText(p.get_start_date())
        service_duration = p.get_service_duration() / (86400 * 7)
        self._info_service_duration.setText(f"{service_duration:.1f} weeks")
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
