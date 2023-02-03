from ColourKey2DWidget import ColourKey2DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from NineBoxSunburstOrgWidget import NineBoxSunburstOrgWidget, nine_box_colours

class NineBoxInfoWidget(InfoOrgKeyWidget):
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_nine_box_potential = self._add_info_text("9-box Grid Potential")
        self._info_nine_box_performance = self._add_info_text("9-box Grid Performance")
        legend = ColourKey2DWidget(nine_box_colours, "9 Box Counts")
        self._org_widget = SunburstOrgKeyWidget(NineBoxSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
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
