from abc import abstractmethod
from PySide6 import QtWidgets

class InfoWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._layout = None

    def _add_info_text(self, text):
        info_layout = QtWidgets.QGridLayout()
        info_layout.addWidget(QtWidgets.QLabel(text), 0, 0, 1, 1)
        info_widget = QtWidgets.QLabel("")
        info_layout.addWidget(info_widget, 0, 1, 1, 4)
        self._layout.addLayout(info_layout)
        return info_widget

    @abstractmethod
    def set_locations(self, locations):
        pass

    @abstractmethod
    def set_people(self, people):
        pass

    @abstractmethod
    def set_uen(self, uen):
        pass

    @abstractmethod
    def render_uen(self):
        pass

    @abstractmethod
    def set_redacted(self, is_redacted):
        pass