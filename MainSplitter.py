from PySide6 import QtWidgets

class MainSplitter(QtWidgets.QSplitter):
    """
    A wrapper around QSplitter, designed solely to let QSS style things.
    """
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
