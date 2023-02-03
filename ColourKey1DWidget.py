from PySide6 import QtWidgets
from ColourBoxWidget import ColourBoxWidget
from ColourBoxLabelWidget import ColourBoxLabelWidget

class ColourKey1DWidget(QtWidgets.QFrame):
    """
    A widget class used to draw colour keys in 1 dimension.
    """
    def __init__(self, colour_dict, count_key = None) -> None:
        super().__init__()
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setColumnMinimumWidth(1, 80)
        self._people = {}
        self._label_widgets = []
        self._colour_box_widgets = []
        self._count_key = count_key

        row = 0
        for cd in colour_dict:
            label_widget = ColourBoxLabelWidget(cd)
            self._layout.addWidget(label_widget, row, 0)
            self._label_widgets.append(label_widget)

            colour_widget = ColourBoxWidget("")
            colour_widget.set_background_colour(colour_dict[cd])
            self._layout.addWidget(colour_widget, row, 1)
            self._colour_box_widgets.append(colour_widget)

            row += 1

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)

    def set_labels(self, labels):
        for i in range(len(self._label_widgets)):
            self._label_widgets[i].setText(labels[i])

    def set_people(self, people):
        self._people = people

    def set_uen(self, uen):
        if self._count_key is None:
            return

        for i in range(len(self._colour_box_widgets)):
            self._colour_box_widgets[i].setText(str(self._people[uen][self._count_key][i]))
