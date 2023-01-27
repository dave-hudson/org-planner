from PySide6 import QtWidgets

class PersonWidget(QtWidgets.QWidget):
    """
    A wrapper around QWidget, designed solely to let QSS style things.
    """
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
