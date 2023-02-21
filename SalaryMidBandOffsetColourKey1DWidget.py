from ColourKey1DWidget import ColourKey1DWidget

class SalaryMidBandOffsetColourKey1DWidget(ColourKey1DWidget):
    """
    A widget class used to draw a colour key for salary mid-band offset charts.
    """
    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            counts = self._people[uen].get_salary_mid_band_offset_counts(self._people)
            self._colour_box_widgets[i].setText(str(counts[i]))
