from ColourKey1DWidget import ColourKey1DWidget

class GenderColourKey1DWidget(ColourKey1DWidget):
    """
    A widget class used to draw a colour key for gender charts.
    """
    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            counts = self._people[uen].get_gender_counts(self._people)
            self._colour_box_widgets[i].setText(str(counts[i]))
