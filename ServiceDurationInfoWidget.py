from PySide6 import QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from ServiceDurationSunburstOrgWidget import ServiceDurationSunburstOrgWidget, service_duration_colours

class ServiceDurationInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._is_manager = False

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._info_start_date = self._add_info_text("Start Date")
        self._info_service_duration = self._add_info_text("Service Duration (weeks)")
        legend = ColourKey1DWidget(service_duration_colours)
        self._org_widget = SunburstOrgKeyWidget(ServiceDurationSunburstOrgWidget(), legend)
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

    def render_uen(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]["Person"]

        self._info_start_date.setText(p["Start Date"])
        service_duration = self._people[uen]["Service Duration"] / (86400 * 7)
        self._info_service_duration.setText(str("{:.1f}").format(service_duration))
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
