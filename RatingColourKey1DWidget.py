from ColourKey1DWidget import ColourKey1DWidget

class RatingColourKey1DWidget(ColourKey1DWidget):
    """
    A widget class used to draw a colour key for rating charts.
    """
    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            counts = self._people[uen].get_rating_counts(self._people)
            self._colour_box_widgets[i].setText(str(counts[i]))
