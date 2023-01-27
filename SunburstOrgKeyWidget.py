from PySide6 import QtWidgets

class SunburstOrgKeyWidget(QtWidgets.QWidget):
    def __init__(self, org_widget, key_widget) -> None:
        super().__init__()

        self._org_widget = org_widget
        self._key_widget = key_widget
        self._is_manager = False
        self._is_redacted = False

        hbox = QtWidgets.QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(org_widget)
        hbox_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        hbox.addItem(hbox_spacer)
        hbox_vbox = QtWidgets.QVBoxLayout()
        hbox_vbox.setContentsMargins(0, 0, 0, 0)
        hbox_vbox_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        hbox_vbox.addItem(hbox_vbox_spacer)
        if key_widget != None:
            hbox_vbox.addWidget(key_widget)

        hbox.addLayout(hbox_vbox)
        self.setLayout(hbox)

    def set_people(self, people):
        self._org_widget.set_people(people)
        if self._key_widget:
            self._key_widget.set_people(people)

    def set_uen(self, uen, is_manager):
        self._is_manager = is_manager
        self.setVisible(is_manager and not self._is_redacted)
        self._org_widget.set_uen(uen)
        if self._key_widget:
            self._key_widget.set_uen(uen)

    def set_redacted(self, is_redacted):
        self._is_redacted = is_redacted
        self.setVisible(self._is_manager and not is_redacted)
