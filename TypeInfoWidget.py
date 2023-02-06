from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from TypeSunburstOrgWidget import TypeSunburstOrgWidget, type_colours

class TypeInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about employee type.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_type = self._add_info_text("Type")
        legend = ColourKey1DWidget(type_colours, "Type Counts")
        self._org_widget = SunburstOrgKeyWidget(TypeSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]["Person"]
        self._info_type.setText(p["Employments"][-1]["Employment"])
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
