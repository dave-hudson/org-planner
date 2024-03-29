from InfoOrgKeyWidget import InfoOrgKeyWidget
from LocationColourKey1DWidget import LocationColourKey1DWidget
from LocationSunburstOrgWidget import LocationSunburstOrgWidget, location_colours
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class LocationInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display location information.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_location = self._add_info_text("Location")
        legend = LocationColourKey1DWidget(location_colours)
        self._org_widget = SunburstOrgKeyWidget(LocationSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]

        location = "None"
        if p.has_location():
            location = p.get_location()

        self._info_location.setText(location)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
