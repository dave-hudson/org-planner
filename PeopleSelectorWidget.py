from PySide6 import QtWidgets

class PeopleSelectorWidget(QtWidgets.QWidget):
    """
    This widget class wraps a list and a tree view of all the people within
    the org.  It's used to make it easy to hide one or the other and thus
    let the app use either view.
    """
    def __init__(self, parent, list_widget, tree_widget) -> None:
        super().__init__(parent)

        vbox = QtWidgets.QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(list_widget)
        vbox.addWidget(tree_widget)
        self.setLayout(vbox)
