from ColourKey1DWidget import ColourKey1DWidget
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from InfoOrgKeyWidget import InfoOrgKeyWidget
from GradeSunburstOrgWidget import GradeSunburstOrgWidget, grade_colours

class GradeInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display information about grade structures.
    """
    def __init__(self) -> None:
        super().__init__()

        self._info_grade = self._add_info_text("Grade")
        legend = ColourKey1DWidget(grade_colours, "Grade Counts")
        self._org_widget = SunburstOrgKeyWidget(GradeSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager

        p = self._people[uen]

        grade = "None"
        if "Grades" in p.keys():
            grade = p["Grades"][-1]["Grade"]

        self._info_grade.setText(grade)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        pass
