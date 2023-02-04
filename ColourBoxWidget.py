from PySide6 import QtWidgets

class ColourBoxWidget(QtWidgets.QLabel):
    """
    A widget class used to draw coloured boxes with text in them.
    """
    def __init__(self, text) -> None:
        super().__init__(text)
        self.setAutoFillBackground(True)
        self.setMargin(4)

    def set_background_colour(self, colour):
        # Set the text colour based on the intensity of the red and green
        # components of the background colour.  We ignore blue!
        if colour[0] + colour[1] > 0xc0:
            ct = "black"
        else:
            ct = "white"

        qss = "background-color: rgb({colour[0]}, {colour[1]}, {colour[2]}); color: {ct}"
        self.setStyleSheet(qss)
