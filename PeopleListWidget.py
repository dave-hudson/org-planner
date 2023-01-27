from PySide6 import QtWidgets

class PeopleListWidget(QtWidgets.QListWidget):
    """
    A wrapper around QListWidget, designed solely to let QSS style things.
    """
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
