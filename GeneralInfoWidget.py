from PySide6 import QtGui, QtWidgets
from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoWidget import InfoWidget

class GeneralInfoWidget(InfoWidget):
    def __init__(self) -> None:
        super().__init__()

        self._people = {}
        self._uen = 0

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        heading_font = QtGui.QFont()
        heading_font.setBold(True)
        heading_font.setPointSize(heading_font.pointSize() * 2)

        self._info_name = QtWidgets.QLabel("")
        self._info_name.setFont(heading_font)
        self._layout.addWidget(self._info_name)
        self._layout.addWidget(QtWidgets.QLabel(""))

        self._info_uen = self._add_info_text("UEN")
        self._info_supervisor_uen = self._add_info_text("Supervisor UEN")
        self._info_percentage_time = self._add_info_text("FTE (%)")

    def set_locations(self, locations):
        pass

    def set_people(self, people):
        self._people = people

    def set_uen(self, uen):
        self._uen = uen

    def update_contents(self):
        uen = self._uen
        p = self._people[uen]["Person"]

        self._info_name.setText(p["Name"])
        self._info_uen.setText(str(p["UEN"]))
        supervisor_uen = "N/A"
        if "Supervisor UEN" in p.keys():
            supervisor = p["Supervisor UEN"]
            supervisor_uen = str("{:d} ({:s})").format(supervisor, self._people[supervisor]["Person"]["Name"])

        self._info_supervisor_uen.setText(supervisor_uen)

        percentage_time = 100
        if "Percentage Time" in p.keys():
            percentage_time = p["Percentage Time"]

        self._info_percentage_time.setText(str(percentage_time))

    def set_redacted(self, is_redacted):
        pass
