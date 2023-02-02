from PySide6 import QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from LocationSunburstOrgWidget import LocationSunburstOrgWidget, location_colours

class LocationInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._is_manager = False

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._info_location = self._add_info_text("Location")
        legend = ColourKey1DWidget(location_colours, "Location Counts")
        self._org_widget = SunburstOrgKeyWidget(LocationSunburstOrgWidget(), legend)
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

    def set_zoom(self, zoom_factor):
        self._org_widget.set_zoom(zoom_factor)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]["Person"]

        location = "None"
        if "Locations" in p.keys():
            location = p["Locations"][-1]["Location"]

        self._info_location.setText(location)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
