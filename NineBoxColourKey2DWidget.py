from ColourKey2DWidget import ColourKey2DWidget

class NineBoxColourKey2DWidget(ColourKey2DWidget):
    """
    A widget class used to draw a colour key for 9-box charts.
    """
    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            for j in range(len(self._colour_box_widgets[i])):
                counts = self._people[uen].get_nine_box_counts(self._people)
                self._colour_box_widgets[i][j].setText(str(counts[i][j]))
