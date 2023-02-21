from ColourKey1DWidget import ColourKey1DWidget

class SalaryColourKey1DWidget(ColourKey1DWidget):
    """
    A widget class used to draw a colour key for salary charts.
    """
    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            counts = self._people[uen].get_salary_counts(self._people)
            self._colour_box_widgets[i].setText(str(counts[i]))
