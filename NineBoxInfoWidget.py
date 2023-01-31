from PySide6 import QtWidgets
from ColourKey2DWidget import ColourKey2DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget
from NineBoxSunburstOrgWidget import NineBoxSunburstOrgWidget, nine_box_colours

class NineBoxInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0
        self._is_manager = False
        self._hide_sensitive_data = True

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._info_nine_box_potential = self._add_info_text("9-box Grid Potential")
        self._info_nine_box_performance = self._add_info_text("9-box Grid Performance")
        legend = ColourKey2DWidget(nine_box_colours, "9 Box Counts")
        self._org_widget = SunburstOrgKeyWidget(NineBoxSunburstOrgWidget(), legend)
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

        nine_box_potential = "None"
        nine_box_performance = "None"
        if self._hide_sensitive_data:
            nine_box_potential = "Hidden"
            nine_box_performance = "Hidden"
        else:
            if "9 Box" in p.keys():
                nine_box_potential = p["9 Box"][-1]["Potential"]
                nine_box_performance = p["9 Box"][-1]["Performance"]

        self._info_nine_box_potential.setText(nine_box_potential)
        self._info_nine_box_performance.setText(nine_box_performance)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
