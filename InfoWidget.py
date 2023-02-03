from abc import abstractmethod
from PySide6 import QtWidgets, QtCore

class InfoWidget(QtWidgets.QWidget):
    person_clicked = QtCore.Signal(int)

    def __init__(self) -> None:
        super().__init__()

        self._layout = None

    def _add_info_text(self, text):
        # Add a text description and a placeholder for a value within the
        # widget.  Returns the widget for the value.
        info_layout = QtWidgets.QGridLayout()
        info_layout.addWidget(QtWidgets.QLabel(text), 0, 0, 1, 1)
        info_widget = QtWidgets.QLabel("")
        info_layout.addWidget(info_widget, 0, 1, 1, 10)
        info_layout.setColumnMinimumWidth(0, 240)
        self._layout.addLayout(info_layout)
        return info_widget

    def _person_clicked(self, person_uen):
        # Handler for propagating "person clicked" events.  We re-emit
        # a new signal to the next level up.
        self.person_clicked.emit(person_uen)

    @abstractmethod
    def set_locations(self, locations):
        """
        Sets the location data used to render this widget.
        """

    @abstractmethod
    def set_people(self, people, top_level_uen):
        """
        Sets the people data used to render this widget.
        """

    @abstractmethod
    def set_uen(self, uen):
        """
        Sets the UEN that this widget should display.
        """

    @abstractmethod
    def set_zoom(self, zoom_factor):
        """
        Sets the zoom factor to use with the widget.
        """

    @abstractmethod
    def update_contents(self):
        """
        Update the contents of the widget.
        """

    @abstractmethod
    def set_redacted(self, is_redacted):
        """
        Sets the "redacted" status of the widget.  If the widget is redacted,
        then all it's contents are marked as hidden.
        """
