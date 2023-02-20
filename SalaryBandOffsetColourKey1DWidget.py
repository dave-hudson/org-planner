from ColourKey1DWidget import ColourKey1DWidget

class SalaryBandOffsetColourKey1DWidget(ColourKey1DWidget):
    """
    A widget class used to draw a colour key for salary band offset charts.
    """
    def __init__(self, colour_dict) -> None:
        super().__init__(colour_dict)

    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            self._colour_box_widgets[i].setText(str(self._people[uen].get_salary_band_offset_counts()[i]))
