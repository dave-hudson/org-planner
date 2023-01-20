import json
import math
import sys
import time
from PySide6 import QtCore, QtGui, QtWidgets

location_colours = {
    "UK": [0xff, 0x40, 0x33],
    "Ireland": [0x70, 0xe0, 0x2c],
    "India": [0xf0, 0xf0, 0x30],
    "Bulgaria": [0x40, 0xcc, 0xff],
    "Singapore": [0xff, 0x99, 0x33],
    "USA": [0xcc, 0x33, 0xff]
}

grade_colours = {
    "A": [0xff, 0x40, 0x33],
    "B": [0xff, 0x99, 0x33],
    "C.H": [0xff, 0xff, 0x33],
    "C.L": [0xe0, 0xe0, 0x2c],
    "C": [0xe0, 0xe0, 0x2c],
    "D.H": [0x99, 0xff, 0x33],
    "D.L": [0x70, 0xe0, 0x2c],
    "D": [0x80, 0xe0, 0x2c],
    "E.H": [0x33, 0xff, 0xff],
    "E.L": [0x40, 0xcc, 0xff],
    "E": [0x40, 0xcc, 0xff],
    "F": [0xe0, 0x80, 0xff],
    "G": [0xcc, 0x33, 0xff]
}

gender_colours = {
    "M": [0x40, 0xc0, 0xff],
    "F": [0xff, 0x80, 0x80],
    "NB": [0xc0, 0xc0, 0x40]
}

nine_box_colours = {
    "High": {
        "Low": [0xff, 0xff, 0x40],
        "Medium": [0xa0, 0xff, 0xa0],
        "High": [0x40, 0xff, 0xff]
    },
    "Medium": {
        "Low": [0xff, 0xa0, 0x40],
        "Medium": [0xa0, 0xa0, 0xa0],
        "High": [0x40, 0xa0, 0xff]
    },
    "Low": {
        "Low": [0xff, 0x40, 0x40],
        "Medium": [0xa0, 0x40, 0xa0],
        "High": [0x40, 0x40, 0xff]
    }
}

rating_colours = {
    "1": [0x40, 0xa0, 0xff],
    "2": [0x40, 0xff, 0x40],
    "3": [0xff, 0xff, 0x40],
    "4": [0xff, 0xa0, 0x40],
    "5": [0xff, 0x40, 0x40]
}

salary_colours = {
    "10000": [0x20, 0x20, 0xff],
    "17783": [0x3c, 0x3c, 0xe4],
    "31600": [0x58, 0x58, 0xd8],
    "56234": [0x74, 0x74, 0xac],
    "100000": [0x90, 0x90, 0x90],
    "177830": [0xac, 0xac, 0x74],
    "316000": [0xc8, 0xc8, 0x58],
    "562340": [0xe4, 0xe4, 0x3c],
    "1000000": [0xff, 0xff, 0x20]
}

rollup_salary_colours = {
    "10000": [0x20, 0xff, 0x20],
    "31600": [0x3c, 0xe4, 0x3c],
    "100000": [0x58, 0xd8, 0x58],
    "316000": [0x74, 0xac, 0x74],
    "1000000": [0x90, 0x90, 0x90],
    "3160000": [0xac, 0x74, 0xac],
    "10000000": [0xc8, 0x58, 0xc8],
    "31600000": [0xe4, 0x3c, 0xe4],
    "100000000": [0xff, 0x20, 0xff]
}

fx_rates = {
    "UK": 1.33,
    "Ireland": 1.16,
    "India": 0.014,
    "Bulgaria": 1.16,
    "Singapore": 0.76,
    "USA": 1.0
}

team_colours_list = [
    [0xff, 0xc0, 0xc0],
    [0xc0, 0xff, 0xc0],
    [0xc0, 0xc0, 0xff],
    [0xff, 0xff, 0xc0],
    [0xc0, 0xff, 0xff],
    [0xff, 0xc0, 0xff],
    [0xc0, 0x80, 0x80],
    [0x80, 0xc0, 0x80],
    [0x80, 0x80, 0xc0],
    [0xc0, 0xc0, 0x80],
    [0x80, 0xc0, 0xc0],
    [0xc0, 0x80, 0xc0],
    [0x80, 0x40, 0x40],
    [0x40, 0x80, 0x40],
    [0x40, 0x40, 0x80],
    [0x80, 0x80, 0x40],
    [0x40, 0x80, 0x80],
    [0x80, 0x40, 0x80],
    [0x40, 0x00, 0x00],
    [0x00, 0x40, 0x00],
    [0x00, 0x00, 0x40],
    [0x40, 0x40, 0x00],
    [0x00, 0x40, 0x40],
    [0x40, 0x00, 0x40],
    [0xff, 0xff, 0xff],
    [0xc0, 0xc0, 0xc0],
    [0x80, 0x80, 0x80],
    [0x40, 0x40, 0x40],
    [0x00, 0x00, 0x00]
]

type_colours_list = [
    [0x60, 0xc0, 0x60],
    [0xc0, 0x60, 0x60],
    [0x60, 0x60, 0xc0],
    [0x60, 0xc0, 0xc0],
    [0xc0, 0xc0, 0x60],
    [0xc0, 0x60, 0xc0],
    [0xc0, 0xc0, 0xc0],
    [0x00, 0x00, 0x00]
]

class HLine(QtWidgets.QFrame):
    """
    A widget class used to insert horizontal dividers between other widgets.
    """
    def __init__(self):
        super().__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Plain)

class ColourBoxWidget(QtWidgets.QLabel):
    def __init__(self, text, colour) -> None:
        super().__init__(text)
        self.setAutoFillBackground(True)
        self.setMargin(4)

        palette = self.palette()
        cb = QtGui.QColor(colour[0], colour[1], colour[2], 0xff)
        palette.setColor(QtGui.QPalette.Window, cb)
        if colour[0] + colour[1] + colour[2] > 0x100:
            ct = QtGui.QColor(0x00, 0x00, 0x00, 0xff)
        else:
            ct = QtGui.QColor(0xff, 0xff, 0xff, 0xff)

        palette.setColor(QtGui.QPalette.WindowText, ct)
        self.setPalette(palette)

class ColourKey1DWidget(QtWidgets.QWidget):
    """
    A widget class used to draw colour keys in 1 dimension.
    """
    def __init__(self, colour_dict, count_key = None) -> None:
        super().__init__()
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setColumnMinimumWidth(1, 80)
        self._people = {}
        self._colour_box_widgets = []
        self._count_key = count_key

        row = 0
        for cd in colour_dict:
            label_widget = ColourBoxWidget(cd, [0x20, 0x20, 0x20])
            self._layout.addWidget(label_widget, row, 0)

            colour_widget = ColourBoxWidget("", colour_dict[cd])
            self._layout.addWidget(colour_widget, row, 1)
            self._colour_box_widgets.append(colour_widget)

            row += 1

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)

    def set_people(self, people):
        self._people = people

    def set_uen(self, uen):
        if self._count_key == None:
            return

        for i in range(len(self._colour_box_widgets)):
            self._colour_box_widgets[i].setText(str(self._people[uen][self._count_key][i]))

class ColourKey2DWidget(QtWidgets.QWidget):
    """
    A widget class used to draw colour keys in 2 dimensions.
    """
    def __init__(self, colour_dict, count_key = None) -> None:
        super().__init__()
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._people = {}
        self._colour_box_widgets = []
        self._count_key = count_key

        col = 1
        for cdj in colour_dict["Low"]:
            self._layout.setColumnMinimumWidth(col, 80)

            colour_widget = ColourBoxWidget(cdj, [0x20, 0x20, 0x20])
            self._layout.addWidget(colour_widget, 0, col)

            col += 1

        row = 1
        for cdi in colour_dict:
            label_widget = ColourBoxWidget(cdi, [0x20, 0x20, 0x20])
            self._layout.addWidget(label_widget, row, 0)

            col = 1
            widget_list = []
            for cdj in colour_dict[cdi]:
                colour_widget = ColourBoxWidget("", colour_dict[cdi][cdj])
                self._layout.addWidget(colour_widget, row, col)
                widget_list.append(colour_widget)

                col += 1

            self._colour_box_widgets.append(widget_list)
            row += 1

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)

    def set_people(self, people):
        self._people = people

    def set_uen(self, uen):
        if self._count_key == None:
            return

        for i in range(len(self._colour_box_widgets)):
            for j in range(len(self._colour_box_widgets[i])):
                self._colour_box_widgets[i][j].setText(str(self._people[uen][self._count_key][i][j]))

class SunburstOrgWidget(QtWidgets.QWidget):
    """
    A widget class used to draw sunburt org charts.
    """
    def __init__(self, render_type) -> None:
        super().__init__()
        self._people = {}
        self._uen = 0
        self._render_type = render_type

    def _scan_depth(self, supervisor):
        org_depth = self._people[supervisor]["Org Depth"]
        for i in self._people[supervisor]["Direct Reports"]:
            d = self._scan_depth(i)
            if d > org_depth:
                org_depth = d

        return org_depth

    def _setup_brush(self, painter, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if self._render_type == 0:
            if "Locations" in p["Person"].keys():
                location = p["Person"]["Locations"][-1]["Location"]
                if location in location_colours:
                    colours = location_colours[location]
        elif self._render_type == 1:
            if "Grades" in p["Person"].keys():
                grade = p["Person"]["Grades"][-1]["Grade"]
                if grade in grade_colours:
                    colours = grade_colours[grade]
        elif self._render_type == 2:
            if "Gender" in p["Person"].keys():
                gender = p["Person"]["Gender"]
                if gender in gender_colours:
                    colours = gender_colours[gender]
        elif self._render_type == 3:
                base_colour = int(0xff * p["Service Duration Fraction"])
                colours = [0xff, 0xff - base_colour, 0xff - base_colour, 0xff]
        elif self._render_type == 4:
            if "9 Box" in p["Person"].keys():
                nine_box_potential = p["Person"]["9 Box"][-1]["Potential"]
                nine_box_performance = p["Person"]["9 Box"][-1]["Performance"]
                if nine_box_potential in nine_box_colours:
                    potential_colours = nine_box_colours[nine_box_potential]
                    if nine_box_performance in potential_colours:
                        colours = potential_colours[nine_box_performance]
        elif self._render_type == 5:
            if "Ratings" in p["Person"].keys():
                rating = str(p["Person"]["Ratings"][-1]["Rating"])
                if rating in rating_colours:
                    colours = rating_colours[rating]
        elif self._render_type == 6:
            if "Salaries" in p["Person"].keys():
                salary = p["Person"]["Salaries"][-1]["Salary"]
                salary_usd = salary * fx_rates[p["Person"]["Locations"][-1]["Location"]]
                log_salary_usd = 0
                if salary > 0:
                    log_salary_usd = math.log10(salary_usd) - 4

                base_colour = int(0x70 * log_salary_usd)
                colours = [0x20 + base_colour, 0x20 + base_colour, 0xff - base_colour, 0xff]
        elif self._render_type == 7:
            rollup_salary = p["Rollup Salaries"]
            if rollup_salary > 0:
                log_rollup_salary = math.log10(rollup_salary) - 4
                base_colour = int(0x38 * log_rollup_salary)
                colours = [0x20 + base_colour, 0xff - base_colour, 0x20 + base_colour, 0xff]
        elif self._render_type == 8:
            if "Team" in p["Person"].keys():
                team = p["Person"]["Team"]
                if team in team_colours:
                    colours = team_colours[team]
        else:
            if "Type" in p["Person"].keys():
                type = p["Person"]["Type"]
                if type in type_colours:
                    colours = type_colours[type]

        brush = QtGui.QBrush(QtGui.QColor(colours[0], colours[1], colours[2], 0xff))
        painter.setBrush(brush)

    def _recurse_draw_widget(self, painter, supervisor_uen, depth, start_angle, start_arc):
        supervisor_person = self._people[supervisor_uen]

        angle = start_angle
        for i in supervisor_person["Direct Reports"]:
            radius = (depth + 1) * self._ring_width
            p = self._people[i]
            sf = p["Supervisor Fraction"]
            arc = sf * start_arc
            self._recurse_draw_widget(painter, i, depth + 1, angle, arc)
            self._setup_brush(painter, i)

            # If our arc is less than a full circle then we're drawing a pie
            # segment, but if it's a full circle then draw it as an ellipse
            # so we don't end up drawing a chord.
            if arc < 359.9999:
                painter.drawPie(self._spacing + self._max_radius - radius,
                                self._spacing + self._max_radius - radius,
                                radius * 2, radius * 2,
                                (90 + angle) * 16, -arc * 16)
            else:
                painter.drawEllipse(self._spacing + self._max_radius - radius,
                                    self._spacing + self._max_radius - radius,
                                    radius * 2, radius * 2)
            angle -= arc

    def _draw_widget(self, painter):
        if len(self._people) == 0:
            return

        # Recursively draw the outer layers of the org chart.
        self._recurse_draw_widget(painter, self._uen, 1, 0, 360)

        # Then draw the inner-most node.
        self._setup_brush(painter, self._uen)
        painter.drawEllipse(self._spacing + self._max_radius - self._ring_width,
                            self._spacing + self._max_radius - self._ring_width,
                            self._ring_width * 2, self._ring_width * 2)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self._draw_widget(qp)
        qp.end()

    def set_render_type(self, r):
        self._render_type = r
        self.update()

    def set_people(self, people):
        self._people = people

    def set_uen(self, uen):
        self._uen = uen

        supervisor_org_depth = self._people[uen]["Org Depth"]

        # Work out how many layers deep the org goes.
        self._max_depth = self._scan_depth(uen)
        self._ring_width = 60
        self._max_radius = self._ring_width * (self._max_depth - supervisor_org_depth + 1)
        self._spacing = 10

        self.setMinimumSize(2 * (self._spacing + self._max_radius) + 1,
                            2 * (self._spacing + self._max_radius) + 1)
        self.update()


class SunburstOrgKeyWidget(QtWidgets.QWidget):
    def __init__(self, org_widget, key_widget) -> None:
        super().__init__()

        self._org_widget = org_widget
        self._key_widget = key_widget

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
        self.setVisible(is_manager)
        self._org_widget.set_uen(uen)
        if self._key_widget:
            self._key_widget.set_uen(uen)


class PeopleSelectorWidget(QtWidgets.QWidget):
    """
    This widget class wraps a list and a tree view of all the people within
    the org.  It's used to make it easy to hide one or the other and thus
    let the app use either view.
    """
    def __init__(self, list_widget, tree_widget) -> None:
        super().__init__()

        vbox = QtWidgets.QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(list_widget)
        vbox.addWidget(tree_widget)
        self.setLayout(vbox)


class MainWindow(QtWidgets.QMainWindow):
    """
    The main window class for the application.
    """
    def __init__(self) -> None:
        super().__init__()

        self._people = {}

        self._view_type = 0
        self._list_view_action = QtGui.QAction("&List View", self)
        self._list_view_action.setCheckable(True)
        self._list_view_action.setChecked(True)
        self._list_view_action.triggered.connect(self._list_view_checked)
        self._tree_view_action = QtGui.QAction("&Tree View", self)
        self._tree_view_action.setCheckable(True)
        self._tree_view_action.setChecked(False)
        self._tree_view_action.triggered.connect(self._tree_view_checked)

        # Create a menu bar and menu drop-downs.
        menu_bar = QtWidgets.QMenuBar()
        self.setMenuBar(menu_bar)
        edit_menu = menu_bar.addMenu("&View")
        edit_menu.addAction(self._list_view_action)
        edit_menu.addAction(self._tree_view_action)
        edit_menu.addSeparator()

        self._people_list_widget = QtWidgets.QListWidget()
        self._people_list_widget.currentItemChanged.connect(self._people_list_index_changed)
        self._people_list_widget.setFocus()
        self._people_tree_widget = QtWidgets.QTreeWidget()
        self._people_tree_widget.currentItemChanged.connect(self._people_tree_item_changed)
        self._people_tree_widget.setHeaderHidden(True)
        self._people_tree_widget.setHidden(True)
        people_selector_widget = PeopleSelectorWidget(self._people_list_widget, self._people_tree_widget)

        self._side_layout = QtWidgets.QVBoxLayout()

        heading_font = QtGui.QFont()
        heading_font.setBold(True)
        heading_font.setPointSize(heading_font.pointSize() * 2)

        self._info_name = QtWidgets.QLabel("")
        self._info_name.setFont(heading_font)
        self._side_layout.addWidget(self._info_name)
        self._side_layout.addWidget(QtWidgets.QLabel(""))

        self._info_uen = self._add_info_text("UEN")
        self._info_supervisor_uen = self._add_info_text("Supervisor UEN")
        self._info_total_reports = self._add_info_text("Total Reports")

        self._side_layout.addWidget(HLine())
        self._info_team = self._add_info_text("Team")
        self._team_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(8), ColourKey1DWidget(team_colours, "Team Counts"))
        self._side_layout.addWidget(self._team_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_type = self._add_info_text("Type")
        self._type_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(9), ColourKey1DWidget(type_colours, "Type Counts"))
        self._side_layout.addWidget(self._type_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_location = self._add_info_text("Location")
        self._location_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(0), ColourKey1DWidget(location_colours, "Location Counts"))
        self._side_layout.addWidget(self._location_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_grade = self._add_info_text("Grade")
        self._grade_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(1), ColourKey1DWidget(grade_colours, "Grade Counts"))
        self._side_layout.addWidget(self._grade_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_gender = self._add_info_text("Gender")
        self._gender_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(2), ColourKey1DWidget(gender_colours, "Gender Counts"))
        self._side_layout.addWidget(self._gender_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_start_date = self._add_info_text("Start Date")
        self._info_service_duration = self._add_info_text("Service Duration (weeks)")
        self._service_duration_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(3), None)
        self._side_layout.addWidget(self._service_duration_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_nine_box_potential = self._add_info_text("9-box Grid Potential")
        self._info_nine_box_performance = self._add_info_text("9-box Grid Performance")
        self._nine_box_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(4), ColourKey2DWidget(nine_box_colours, "9 Box Counts"))
        self._side_layout.addWidget(self._nine_box_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_rating = self._add_info_text("Rating")
        self._rating_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(5), ColourKey1DWidget(rating_colours, "Rating Counts"))
        self._side_layout.addWidget(self._rating_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_salary = self._add_info_text("Salary")
        self._info_salary_usd = self._add_info_text("Salary (USD)")
        self._salary_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(6), ColourKey1DWidget(salary_colours))
        self._side_layout.addWidget(self._salary_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_rollup_salary_usd = self._add_info_text("Rollup Salary (USD")
        self._rollup_salary_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(7), ColourKey1DWidget(rollup_salary_colours))
        self._side_layout.addWidget(self._rollup_salary_org_widget)

        # Insert a spacer so the layout engine doesn't try to spread out the
        # info panel elements if they take less space than the visible
        # window.
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self._side_layout.addItem(spacer)

        widget = QtWidgets.QWidget()
        widget.setLayout(self._side_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        splitter_widget = QtWidgets.QSplitter()
        splitter_widget.addWidget(people_selector_widget)
        splitter_widget.addWidget(scroll_area)

        self.setCentralWidget(splitter_widget)

    def _add_info_text(self, text):
        info_layout = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout)
        info_layout.addWidget(QtWidgets.QLabel(text), 0, 0)
        info_widget = QtWidgets.QLabel("")
        info_layout.addWidget(info_widget, 0, 1)
        return info_widget

    def _list_view_checked(self, s):
        """
        Called when the "List View" menu item is checked.

        We flip the application view type, flip the checkbox on the
        list/tree view, hide the tree view and unhide the list view.
        """

        self._view_type = 0
        self._list_view_action.setChecked(True)
        self._tree_view_action.setChecked(False)
        self._people_list_widget.setHidden(False)
        self._people_tree_widget.setHidden(True)

        # For UI continuity we take the current selected item from the tree
        # view and select the same entry in the list view.
        tree_selected = self._people_tree_widget.currentItem()
        item = self._people_list_widget.findItems(tree_selected.text(0), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
        self._people_list_widget.setCurrentItem(item[0])
        self._people_list_widget.setFocus()

    def _tree_view_checked(self, s):
        """
        Called when the "Tree View" menu item is checked.

        We flip the application view type, flip the checkbox on the
        list/tree view, hide the list view and unhide the tree view.
        """

        self._view_type = 1
        self._list_view_action.setChecked(False)
        self._tree_view_action.setChecked(True)
        self._people_list_widget.setHidden(True)
        self._people_tree_widget.setHidden(False)

        # For UI continuity we take the current selected item from the list
        # view and select the same entry in the tree view.
        list_selected = self._people_list_widget.currentItem()
        item = self._people_tree_widget.findItems(list_selected.text(), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive)
        self._people_tree_widget.setCurrentItem(item[0])
        self._people_tree_widget.setFocus()

    def _people_list_index_changed(self, list_item):
        for i in self._people:
            if self._people[i]["Person"]["Name"] == list_item.text():
                self.set_uen(i)
                break

    def _people_tree_item_changed(self, tree_item):
        for i in self._people:
            if self._people[i]["Person"]["Name"] == tree_item.text(0):
                self.set_uen(i)
                break

    def _set_people_tree(self, supervisor_uen, supervisor_item):
        for p in self._people[supervisor_uen]["Direct Reports"]:
            twi = QtWidgets.QTreeWidgetItem()
            twi.setText(0, self._people[p]["Person"]["Name"])
            supervisor_item.addChild(twi)
            self._set_people_tree(p, twi)

    def set_people(self, people, uen):
        self._people = people

        for i in people:
            self._people_list_widget.addItem(people[i]["Person"]["Name"])

        self._people_list_widget.sortItems(QtGui.Qt.AscendingOrder)

        top_level = QtWidgets.QTreeWidgetItem()
        top_level.setText(0, people[uen]["Person"]["Name"])
        self._set_people_tree(uen, top_level)
        self._people_tree_widget.insertTopLevelItem(0, top_level)
        self._people_tree_widget.expandAll()

        self._team_org_widget.set_people(people)
        self._type_org_widget.set_people(people)
        self._location_org_widget.set_people(people)
        self._grade_org_widget.set_people(people)
        self._gender_org_widget.set_people(people)
        self._service_duration_org_widget.set_people(people)
        self._nine_box_org_widget.set_people(people)
        self._rating_org_widget.set_people(people)
        self._salary_org_widget.set_people(people)
        self._rollup_salary_org_widget.set_people(people)

        list_selected = self._people_list_widget.item(0)
        self._people_list_widget.setCurrentItem(list_selected)

        self.update()

    def set_uen(self, uen):
        is_manager = False
        if len(self._people[uen]["Direct Reports"]) != 0:
            is_manager = True

        p = self._people[uen]["Person"]
        self._info_name.setText(p["Name"])
        self._info_uen.setText(str(p["UEN"]))
        supervisor_uen = "N/A"
        if "Supervisor UEN" in p.keys():
            supervisor = p["Supervisor UEN"]
            supervisor_uen = str("{:d} ({:s})").format(supervisor, self._people[supervisor]["Person"]["Name"])

        self._info_supervisor_uen.setText(supervisor_uen)
        self._info_total_reports.setText(str(self._people[uen]["Total Reports"]))

        self._info_team.setText(p["Team"])
        self._team_org_widget.set_uen(uen, is_manager)

        self._info_type.setText(p["Type"])
        self._type_org_widget.set_uen(uen, is_manager)

        self._info_location.setText(p["Locations"][-1]["Location"])
        self._location_org_widget.set_uen(uen, is_manager)

        grade = "None"
        if "Grades" in p.keys():
            grade = p["Grades"][-1]["Grade"]

        self._info_grade.setText(grade)
        self._grade_org_widget.set_uen(uen, is_manager)

        gender = "None"
        if "Gender" in p.keys():
            gender = p["Gender"]

        self._info_gender.setText(gender)
        self._gender_org_widget.set_uen(uen, is_manager)

        self._info_start_date.setText(p["Start Date"])
        service_duration = self._people[uen]["Service Duration"] / (86400 * 7)
        self._info_service_duration.setText(str("{:.1f}").format(service_duration))
        self._service_duration_org_widget.set_uen(uen, is_manager)

        nine_box_potential = "None"
        nine_box_performance = "None"
        if "9 Box" in p.keys():
            nine_box_potential = p["9 Box"][-1]["Potential"]
            nine_box_performance = p["9 Box"][-1]["Performance"]

        self._info_nine_box_potential.setText(nine_box_potential)
        self._info_nine_box_performance.setText(nine_box_performance)
        self._nine_box_org_widget.set_uen(uen, is_manager)

        rating = "None"
        if "Ratings" in p.keys():
            rating = str(p["Ratings"][-1]["Rating"])

        self._info_rating.setText(rating)
        self._rating_org_widget.set_uen(uen, is_manager)

        salary = "N/A"
        salary_usd = "N/A"
        if "Salaries" in p.keys():
            salary_val = p["Salaries"][-1]["Salary"]
            salary = str(salary_val)
            salary_usd_val = salary_val * fx_rates[p["Locations"][-1]["Location"]]
            salary_usd = str(int(salary_usd_val))

        self._info_salary.setText(salary)
        self._info_salary_usd.setText(salary_usd)
        self._salary_org_widget.set_uen(uen, is_manager)

        rollup_salary_usd = "N/A"
        rollup_salary_usd_val = int(self._people[uen]["Rollup Salaries"])

        if is_manager:
            rollup_missing_salaries = self._people[uen]["Missing Salaries"]
            rollup_salary_usd = str("{:d} (Missing {:d} people)").format(rollup_salary_usd_val, rollup_missing_salaries)

        self._info_rollup_salary_usd.setText(rollup_salary_usd)
        self._rollup_salary_org_widget.set_uen(uen, is_manager)

        self.update()


def scan_teams_and_types(people):
    teams = []
    types = []

    for i in people:
        team = people[i]["Person"]["Team"]
        if team not in teams:
            teams.append(team)

        type = people[i]["Person"]["Type"]
        if type not in types:
            types.append(type)

    return (teams, types)

def scan_org_tree(people, supervisor_uen, depth):
    # Scan each direct report recursively, computing how deep each person is in
    # the overall org, and how many reports roll up to them in total.
    p = people[supervisor_uen]
    p["Location Counts"] = [0] * len(location_colours)
    p["Team Counts"] = [0] * len(team_colours)
    p["Type Counts"] = [0] * len(type_colours)
    p["Grade Counts"] = [0] * len(grade_colours)
    p["Gender Counts"] = [0] * len(gender_colours)
    p["9 Box Counts"] = [[] for i in range(3)]
    for i in range(3):
        p["9 Box Counts"][i] = [0] * 3
    p["Rating Counts"] = [0] * len(rating_colours)
    p["Total Reports"] = 0
    p["Rollup Salaries"] = 0
    p["Missing Salaries"] = 0

    for i in p["Direct Reports"]:
        scan_org_tree(people, i, depth + 1)
        dr = people[i]

        for j in range(len(p["Team Counts"])):
            p["Team Counts"][j] += dr["Team Counts"][j]

        for j in range(len(p["Type Counts"])):
            p["Type Counts"][j] += dr["Type Counts"][j]

        for j in range(len(p["Location Counts"])):
            p["Location Counts"][j] += dr["Location Counts"][j]

        for j in range(len(p["Grade Counts"])):
            p["Grade Counts"][j] += dr["Grade Counts"][j]

        for j in range(len(p["Gender Counts"])):
            p["Gender Counts"][j] += dr["Gender Counts"][j]

        for j in range(len(p["9 Box Counts"])):
            for k in range(len(p["9 Box Counts"][j])):
                p["9 Box Counts"][j][k] += dr["9 Box Counts"][j][k]

        for j in range(len(p["Rating Counts"])):
            p["Rating Counts"][j] += dr["Rating Counts"][j]

        p["Total Reports"] += (dr["Total Reports"] + 1)
        p["Rollup Salaries"] += dr["Rollup Salaries"]
        p["Missing Salaries"] += dr["Missing Salaries"]

    team = p["Person"]["Team"]
    p["Team Counts"][list(team_colours).index(team)] += 1

    type = p["Person"]["Type"]
    p["Type Counts"][list(type_colours).index(type)] += 1

    location = p["Person"]["Locations"][-1]["Location"]
    p["Location Counts"][list(location_colours).index(location)] += 1

    if "Grades" in p["Person"].keys():
        grade = p["Person"]["Grades"][-1]["Grade"]
        p["Grade Counts"][list(grade_colours).index(grade)] += 1

    if "Gender" in p["Person"].keys():
        gender = p["Person"]["Gender"]
        p["Gender Counts"][list(gender_colours).index(gender)] += 1

    if "9 Box" in p["Person"].keys():
        nine_box_potential = p["Person"]["9 Box"][-1]["Potential"]
        nine_box_potential_index = list(nine_box_colours).index(nine_box_potential)
        nine_box_performance = p["Person"]["9 Box"][-1]["Performance"]
        nine_box_performance_index = list(nine_box_colours[nine_box_potential]).index(nine_box_performance)
        p["9 Box Counts"][nine_box_potential_index][nine_box_performance_index] += 1

    if "Ratings" in p["Person"].keys():
        rating = str(p["Person"]["Ratings"][-1]["Rating"])
        p["Rating Counts"][list(rating_colours).index(rating)] += 1

    p["Org Depth"] = depth

    # Scan each direct report, but this time compute the fraction of the overall
    # team their subteam represents.
    drs = p["Direct Reports"]
    num_reports = p["Total Reports"]
    for i in drs:
        people[i]["Supervisor Fraction"] = (people[i]["Total Reports"] + 1) / num_reports

    # Sort the direct reports to put the one with the largest fraction of the
    # org first.
    for i in range(len(drs)):
        for j in range(len(drs) - i - 1):
            if people[drs[j]]["Supervisor Fraction"] < people[drs[j + 1]]["Supervisor Fraction"]:
                t = drs[j + 1]
                drs[j + 1] = drs[j]
                drs[j] = t

    # Then sort any direct reports from the same team to cluster them.  While
    # this slightly undoes the sort it's a more natural view over the org,
    # placing people who do the same sorts of things in one grouping.
    for i in range(1, len(drs)):
        if people[drs[i - 1]]["Person"]["Team"] == people[drs[i]]["Person"]["Team"]:
            continue

        for j in range(i + 1, len(drs)):
            if people[drs[i - 1]]["Person"]["Team"] == people[drs[j]]["Person"]["Team"]:
                for k in range(j, i, -1):
                    t = drs[j - 1]
                    drs[j - 1] = drs[j]
                    drs[j] = t

    start_date = p["Person"]["Start Date"]
    t = time.strptime(start_date, "%Y-%m-%d")
    ot = time.strptime("2016-01-01", "%Y-%m-%d")
    cur_time = time.time()
    org_elapsed_time = cur_time - time.mktime(ot)
    worked_time = cur_time - time.mktime(t)
    p["Service Duration"] = cur_time - time.mktime(t)
    p["Service Duration Fraction"] = worked_time / org_elapsed_time

    if "Salaries" not in p["Person"].keys():
        p["Missing Salaries"] += 1
    else:
        salary = p["Person"]["Salaries"][-1]["Salary"]
        salary_usd = salary * fx_rates[location]
        p["Rollup Salaries"] += salary_usd

def scan_json(json_data):
    people = {}
    top_level = 0
    failed = False

    all_people_list = json_data["People"]
    for i in all_people_list:
        uen = i["UEN"]
        people[uen] = {}
        people[uen]["Person"] = i
        people[uen]["Direct Reports"] = []

    for i in all_people_list:
        uen = i["UEN"]
        if "Supervisor UEN" not in i.keys():
            if top_level == 0:
                top_level = uen
            else:
                print(i["Name"], "does not have a supervisor, but", top_level, "is already set as top-level")
                failed = True
        else:
            supervisor_uen = i["Supervisor UEN"]
            people[supervisor_uen]["Direct Reports"].append(uen)

    return (failed, people, top_level)

json_file_path = r'people.json'
with open(json_file_path, encoding = 'utf-8') as user_file:
    json_data = json.load(user_file)

fail, all_people, uen = scan_json(json_data)
if fail:
    exit()

all_teams, all_types = scan_teams_and_types(all_people)
all_teams.sort()

team_colours = {}
ci = 0
for i in all_teams:
    team_colours[i] = team_colours_list[ci]
    ci += 1

type_colours = {}
ci = 0
for i in all_types:
    type_colours[i] = type_colours_list[ci]
    ci += 1

scan_org_tree(all_people, uen, 0)
all_people[uen]["Supervisor Fraction"] = 1

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.set_people(all_people, uen)
window.show()
app.exec()
