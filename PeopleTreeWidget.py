from PySide6 import QtWidgets

class PeopleTreeWidget(QtWidgets.QTreeWidget):
    """
    A wrapper around QTreeWidget, designed solely to let QSS style things.
    """
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
