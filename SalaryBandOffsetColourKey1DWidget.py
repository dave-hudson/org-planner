from ColourKey1DWidget import ColourKey1DWidget

class SalaryBandOffsetColourKey1DWidget(ColourKey1DWidget):
    """
    A widget class used to draw a colour key for salary band offset charts.
    """
    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            counts = self._people[uen].get_salary_band_offset_counts(self._people)
            self._colour_box_widgets[i].setText(str(counts[i]))
