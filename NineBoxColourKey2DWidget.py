from ColourKey2DWidget import ColourKey2DWidget

class NineBoxColourKey2DWidget(ColourKey2DWidget):
    """
    A widget class used to draw a colour key for 9-box charts.
    """
    def __init__(self, colour_dict) -> None:
        super().__init__(colour_dict)

    def set_uen(self, uen):
        for i in range(len(self._colour_box_widgets)):
            for j in range(len(self._colour_box_widgets[i])):
                self._colour_box_widgets[i][j].setText(
                    str(self._people[uen].get_nine_box_counts()[i][j])
                )
