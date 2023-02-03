from PySide6 import QtGui, QtWidgets
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from GeneralSunburstOrgWidget import GeneralSunburstOrgWidget

class GeneralInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display general information about a person.
    """
    def __init__(self) -> None:
        super().__init__()

        self._supervisor_uen = 0

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
        self._org_only_widget = GeneralSunburstOrgWidget()
        self._org_widget = SunburstOrgKeyWidget(self._org_only_widget, None)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        p = self._people[uen]["Person"]

        self._info_name.setText(p["Name"])
        self._info_uen.setText(str(p["UEN"]))
        supervisor_uen = "N/A"
        if "Supervisor UEN" in p.keys():
            supervisor = p["Supervisor UEN"]
            supervisor_uen = str("{:d} ({:s})").format(
                supervisor, self._people[supervisor]["Person"]["Name"]
            )

        self._info_supervisor_uen.setText(supervisor_uen)

        percentage_time = 100
        if "Percentage Time" in p.keys():
            percentage_time = p["Percentage Time"]

        self._info_percentage_time.setText(str(percentage_time))

    def set_people_and_supervisor(self, people, supervisor_uen):
        self._people = people
        self._supervisor_uen = supervisor_uen

        self._org_widget.set_people(people)

    def set_uen(self, uen):
        self._uen = uen

        self._org_widget.set_uen(self._supervisor_uen, True)
        self._org_only_widget.set_ident_uen(uen)

    def set_redacted(self, is_redacted):
        pass
