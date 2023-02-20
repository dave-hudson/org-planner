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

        heading_font = QtGui.QFont()
        heading_font.setBold(True)
        heading_font.setPointSize(heading_font.pointSize() * 2)

        self._info_name = QtWidgets.QLabel("")
        self._info_name.setFont(heading_font)
        self._layout.addWidget(self._info_name)
        self._layout.addWidget(QtWidgets.QLabel(""))

        self._info_uen = self._add_info_text("UEN")
        self._info_email_address = self._add_info_text("Email Address")
        self._info_supervisor_uen = self._add_info_text("Supervisor UEN")
        self._org_only_widget = GeneralSunburstOrgWidget()
        self._org_widget = SunburstOrgKeyWidget(self._org_only_widget, None)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        p = self._people[uen]

        self._info_name.setText(p.get_name())
        self._info_uen.setText(str(p.get_uen()))

        email_address = "N/A"
        if p.has_email_address():
            email_address = p.get_email_address()

        self._info_email_address.setText(email_address)

        supervisor_uen = "N/A"
        if p.has_supervisor():
            supervisor = p.get_supervisor_uen()
            supervisor_uen = str("{:d} ({:s})").format(
                supervisor, self._people[supervisor].get_name()
            )

        self._info_supervisor_uen.setText(supervisor_uen)

    def set_uen(self, uen):
        self._uen = uen

        self._org_widget.set_uen(self._top_level_uen, True)
        self._org_only_widget.set_ident_uen(uen)

    def set_redacted(self, is_redacted):
        pass
