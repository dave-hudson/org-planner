from PySide6 import QtCore, QtGui, QtWidgets

class HLine(QtWidgets.QFrame):
    """
    A widget class used to insert horizontal dividers between other widgets.
    """
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)

