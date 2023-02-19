from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from LocationSunburstOrgWidget import LocationSunburstOrgWidget, location_colours

class LocationInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display location information.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_location = self._add_info_text("Location")
        legend = ColourKey1DWidget(location_colours, "Location Counts")
        self._org_widget = SunburstOrgKeyWidget(LocationSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]

        location = "None"
        if "Locations" in p.keys():
            location = p["Locations"][-1]["Location"]

        self._info_location.setText(location)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
