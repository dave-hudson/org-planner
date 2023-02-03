from PySide6 import QtWidgets
from InfoWidget import InfoWidget

class InfoOrgKeyWidget(InfoWidget):
    """
    A widget class that shows text information, an org chart, and an optional key legend.
    """
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._top_level_uen = 0
        self._is_manager = False
        self._org_widget = None

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

    def set_locations(self, locations):
        self._org_widget.set_locations(locations)

    def set_people(self, people, top_level_uen):
        self._people = people
        self._top_level_uen = top_level_uen
        self._org_widget.set_people(people, top_level_uen)

    def set_uen(self, uen):
        self._uen = uen

        is_manager = False
        if len(self._people[uen]["Direct Reports"]) != 0:
            is_manager = True

        self._is_manager = is_manager
        self._org_widget.set_uen(uen, is_manager)

    def set_zoom(self, zoom_factor):
        self._org_widget.set_zoom(zoom_factor)
