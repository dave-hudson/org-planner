from PySide6 import QtWidgets
from ColourBoxWidget import ColourBoxWidget
from ColourBoxLabelWidget import ColourBoxLabelWidget

class ColourKey2DWidget(QtWidgets.QFrame):
    """
    A widget class used to draw colour keys in 2 dimensions.
    """
    def __init__(self, colour_dict, count_key = None) -> None:
        super().__init__()
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._people = {}
        self._colour_box_widgets = []
        self._count_key = count_key

        col = 1
        for cdj in colour_dict["Low"]:
            self._layout.setColumnMinimumWidth(col, 80)

            colour_widget = ColourBoxLabelWidget(cdj)
            self._layout.addWidget(colour_widget, 0, col)

            col += 1

        row = 1
        for cdi in colour_dict:
            label_widget = ColourBoxLabelWidget(cdi)
            self._layout.addWidget(label_widget, row, 0)

            col = 1
            widget_list = []
            for cdj in colour_dict[cdi]:
                colour_widget = ColourBoxWidget("")
                colour_widget.set_background_colour(colour_dict[cdi][cdj])
                self._layout.addWidget(colour_widget, row, col)
                widget_list.append(colour_widget)

                col += 1

            self._colour_box_widgets.append(widget_list)
            row += 1

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)

    def set_people(self, people):
        self._people = people

    def set_uen(self, uen):
        if self._count_key is None:
            return

        for i in range(len(self._colour_box_widgets)):
            for j in range(len(self._colour_box_widgets[i])):
                self._colour_box_widgets[i][j].setText(str(self._people[uen][self._count_key][i][j]))
