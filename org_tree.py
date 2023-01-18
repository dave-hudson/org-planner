import json
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
    "F": [0xff, 0x80, 0x80]
}

nine_box_colours = {
    "High": {
        "Low": [0xff, 0xff, 0x20],
        "Medium": [0x20, 0xe0, 0x40],
        "High": [0x20, 0x80, 0xe0]
    },
    "Medium": {
        "Low": [0xff, 0xa0, 0x20],
        "Medium": [0xff, 0xff, 0x20],
        "High": [0x20, 0xe0, 0x40]
    },
    "Low": {
        "Low": [0xff, 0x40, 0x40],
        "Medium": [0xff, 0xa0, 0x20],
        "High": [0xff, 0xff, 0x20]
    }
}

rating_colours = {
    "1": [0x20, 0x80, 0xe0],
    "2": [0x20, 0xe0, 0x40],
    "3": [0xff, 0xff, 0x20],
    "4": [0xff, 0xa0, 0x20],
    "5": [0xff, 0x40, 0x40]
}

fx_rates = {
    "UK": 1.33,
    "Ireland": 1.16,
    "India": 0.014,
    "Bulgaria": 1.16,
    "Singapore": 0.76,
    "USA": 1.0
}

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
        ct = QtGui.QColor(0xff, 0xff, 0xff, 0xff)
        palette.setColor(QtGui.QPalette.WindowText, ct)
        self.setPalette(palette)

class ColourKey1DWidget(QtWidgets.QWidget):
    """
    A widget class used to draw colour keys in 1 dimension.
    """
    def __init__(self, colour_dict) -> None:
        super().__init__()
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        self._layout.setColumnMinimumWidth(1, 80)

        row = 0
        for cd in colour_dict:
            label_widget = ColourBoxWidget(cd, [0x20, 0x20, 0x20])
            self._layout.addWidget(label_widget, row, 0)

            colour_widget = ColourBoxWidget("", colour_dict[cd])
            self._layout.addWidget(colour_widget, row, 1)

            row += 1

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)

class ColourKey2DWidget(QtWidgets.QWidget):
    """
    A widget class used to draw colour keys in 2 dimensions.
    """
    def __init__(self, colour_dict) -> None:
        super().__init__()
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)

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
            for cdj in colour_dict[cdi]:
                colour_widget = ColourBoxWidget("", colour_dict[cdi][cdj])
                self._layout.addWidget(colour_widget, row, col)

                col += 1

            row += 1

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(self._layout)

class SunburstOrgWidget(QtWidgets.QWidget):
    """
    A widget class used to draw sunburt org charts.
    """
    def __init__(self, render_type) -> None:
        super().__init__()
        self._people = {}
        self._top_level_supervisor = 0
        self._render_type = render_type

    def _scan_depth(self, supervisor):
        org_depth = self._people[supervisor]["Org Depth"]
        for i in self._people[supervisor]["Direct Reports"]:
            d = self._scan_depth(i)
            if d > org_depth:
                org_depth = d

        return org_depth

    def _setup_brush(self, painter, uen):
        colours = [0x80, 0x80, 0x80]

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
                base_colour = int(0xc0 * p["Service Duration Fraction"])
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
        else:
            if "Salaries" in p["Person"].keys():
                salary = p["Person"]["Salaries"][-1]["Salary"]
                salary_fraction = salary * fx_rates[p["Person"]["Locations"][-1]["Location"]] / 300000
                base_colour = int(0xc0 * salary_fraction)
                colours = [0xff - base_colour, 0xff - base_colour, 0xff, 0xff]

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
        self._recurse_draw_widget(painter, self._top_level_supervisor, 1, 0, 360)

        # Then draw the inner-most node.
        self._setup_brush(painter, self._top_level_supervisor)
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

    def set_supervisor(self, top_level_supervisor):
        self._top_level_supervisor = top_level_supervisor

        supervisor_org_depth = self._people[top_level_supervisor]["Org Depth"]

        # Work out how many layers deep the org goes.
        self._max_depth = self._scan_depth(top_level_supervisor)
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

    def set_supervisor(self, top_level_supervisor):
        self._org_widget.set_supervisor(top_level_supervisor)


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
        menu_bar = QtWidgets.QMenuBar(self)
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

        info_layout0 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout0)

        info_layout0.addWidget(QtWidgets.QLabel("UEN"), 0, 0)
        self._info_uen = QtWidgets.QLabel("")
        info_layout0.addWidget(self._info_uen, 0, 1)
        info_layout0.addWidget(QtWidgets.QLabel("Supervisor UEN"), 1, 0)
        self._info_supervisor_uen = QtWidgets.QLabel("")
        info_layout0.addWidget(self._info_supervisor_uen, 1, 1)
        info_layout0.addWidget(QtWidgets.QLabel("Total Reports"), 2, 0)
        self._info_total_reports = QtWidgets.QLabel("")
        info_layout0.addWidget(self._info_total_reports, 2, 1)

        separator0 = HLine()
        self._side_layout.addWidget(separator0)

        info_layout1 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout1)
        info_layout1.addWidget(QtWidgets.QLabel("Location"), 0, 0)
        self._info_location = QtWidgets.QLabel("")
        info_layout1.addWidget(self._info_location, 0, 1)

        self._location_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(0), ColourKey1DWidget(location_colours))
        self._side_layout.addWidget(self._location_org_widget)

        separator1 = HLine()
        self._side_layout.addWidget(separator1)

        info_layout2 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout2)
        info_layout2.addWidget(QtWidgets.QLabel("Grade"), 0, 0)
        self._info_grade = QtWidgets.QLabel("")
        info_layout2.addWidget(self._info_grade, 0, 1)

        self._grade_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(1), ColourKey1DWidget(grade_colours))
        self._side_layout.addWidget(self._grade_org_widget)

        separator2 = HLine()
        self._side_layout.addWidget(separator2)

        info_layout3 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout3)
        info_layout3.addWidget(QtWidgets.QLabel("Gender"), 0, 0)
        self._info_gender = QtWidgets.QLabel("")
        info_layout3.addWidget(self._info_gender, 0, 1)

        self._gender_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(2), ColourKey1DWidget(gender_colours))
        self._side_layout.addWidget(self._gender_org_widget)

        separator3 = HLine()
        self._side_layout.addWidget(separator3)

        info_layout4 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout4)
        info_layout4.addWidget(QtWidgets.QLabel("Start Date"), 0, 0)
        self._info_start_date = QtWidgets.QLabel("")
        info_layout4.addWidget(self._info_start_date, 0, 1)
        info_layout4.addWidget(QtWidgets.QLabel("Service Duration (weeks)"), 1, 0)
        self._info_service_duration = QtWidgets.QLabel("")
        info_layout4.addWidget(self._info_service_duration, 1, 1)

        self._service_duration_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(3), None)
        self._side_layout.addWidget(self._service_duration_org_widget)

        separator4 = HLine()
        self._side_layout.addWidget(separator4)

        info_layout5 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout5)
        info_layout5.addWidget(QtWidgets.QLabel("9-box Grid Potential"), 0, 0)
        self._info_nine_box_potential = QtWidgets.QLabel("")
        info_layout5.addWidget(self._info_nine_box_potential, 0, 1)
        info_layout5.addWidget(QtWidgets.QLabel("9-box Grid Performance"), 1, 0)
        self._info_nine_box_performance = QtWidgets.QLabel("")
        info_layout5.addWidget(self._info_nine_box_performance, 1, 1)

        self._nine_box_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(4), ColourKey2DWidget(nine_box_colours))
        self._side_layout.addWidget(self._nine_box_org_widget)

        separator5 = HLine()
        self._side_layout.addWidget(separator5)

        info_layout6 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout6)
        info_layout6.addWidget(QtWidgets.QLabel("Rating"), 0, 0)
        self._info_rating = QtWidgets.QLabel("")
        info_layout6.addWidget(self._info_rating, 0, 1)

        self._rating_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(5), ColourKey1DWidget(rating_colours))
        self._side_layout.addWidget(self._rating_org_widget)

        separator6 = HLine()
        self._side_layout.addWidget(separator6)

        info_layout7 = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout7)
        info_layout7.addWidget(QtWidgets.QLabel("Salary"), 0, 0)
        self._info_salary = QtWidgets.QLabel("")
        info_layout7.addWidget(self._info_salary, 0, 1)
        info_layout7.addWidget(QtWidgets.QLabel("Salary (USD)"), 1, 0)
        self._info_salary_usd = QtWidgets.QLabel("")
        info_layout7.addWidget(self._info_salary_usd, 1, 1)
        info_layout7.addWidget(QtWidgets.QLabel("Rollup Salary (USD)"), 2, 0)
        self._info_rollup_salary_usd = QtWidgets.QLabel("")
        info_layout7.addWidget(self._info_rollup_salary_usd, 2, 1)

        self._salary_org_widget = SunburstOrgKeyWidget(SunburstOrgWidget(6), None)
        self._side_layout.addWidget(self._salary_org_widget)

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
                self.set_supervisor(i)
                break

    def _people_tree_item_changed(self, tree_item):
        for i in self._people:
            if self._people[i]["Person"]["Name"] == tree_item.text(0):
                self.set_supervisor(i)
                break

    def _set_people_tree(self, supervisor_uen, supervisor_item):
        for p in self._people[supervisor_uen]["Direct Reports"]:
            twi = QtWidgets.QTreeWidgetItem()
            twi.setText(0, self._people[p]["Person"]["Name"])
            supervisor_item.addChild(twi)
            self._set_people_tree(p, twi)

    def set_people(self, people, top_level_supervisor):
        self._people = people

        for i in people:
            self._people_list_widget.addItem(people[i]["Person"]["Name"])

        self._people_list_widget.sortItems(QtGui.Qt.AscendingOrder)

        top_level = QtWidgets.QTreeWidgetItem()
        top_level.setText(0, people[top_level_supervisor]["Person"]["Name"])
        self._set_people_tree(top_level_supervisor, top_level)
        self._people_tree_widget.insertTopLevelItem(0, top_level)
        self._people_tree_widget.expandAll()

        self._location_org_widget.set_people(people)
        self._grade_org_widget.set_people(people)
        self._gender_org_widget.set_people(people)
        self._service_duration_org_widget.set_people(people)
        self._nine_box_org_widget.set_people(people)
        self._rating_org_widget.set_people(people)
        self._salary_org_widget.set_people(people)

        list_selected = self._people_list_widget.item(0)
        print(list_selected)
        self._people_list_widget.setCurrentItem(list_selected)

        self.update()

    def set_supervisor(self, top_level_supervisor):
        print("set supervisor", top_level_supervisor)
        manager = False
        if len(self._people[top_level_supervisor]["Direct Reports"]) != 0:
            manager = True

        p = self._people[top_level_supervisor]["Person"]
        self._info_name.setText(p["Name"])
        self._info_uen.setText(str(p["UEN"]))
        if "Supervisor UEN" in p.keys():
            self._info_supervisor_uen.setText(str(p["Supervisor UEN"]))

        self._info_total_reports.setText(str(self._people[top_level_supervisor]["Total Reports"]))

        self._info_location.setText(p["Locations"][-1]["Location"])
        self._location_org_widget.set_supervisor(top_level_supervisor)
        self._location_org_widget.setVisible(manager)

        grade = "None"
        if "Grades" in p.keys():
            grade = p["Grades"][-1]["Grade"]

        self._info_grade.setText(grade)
        self._grade_org_widget.set_supervisor(top_level_supervisor)
        self._grade_org_widget.setVisible(manager)

        gender = "None"
        if "Gender" in p.keys():
            gender = p["Gender"]

        self._info_gender.setText(gender)
        self._gender_org_widget.set_supervisor(top_level_supervisor)
        self._gender_org_widget.setVisible(manager)

        self._info_start_date.setText(p["Start Date"])
        service_duration = self._people[top_level_supervisor]["Service Duration"] / (86400 * 7)
        self._info_service_duration.setText(str("{:.1f}").format(service_duration))
        self._service_duration_org_widget.set_supervisor(top_level_supervisor)
        self._service_duration_org_widget.setVisible(manager)

        nine_box_potential = "None"
        nine_box_performance = "None"
        if "9 Box" in p.keys():
            nine_box_potential = p["9 Box"][-1]["Potential"]
            nine_box_performance = p["9 Box"][-1]["Performance"]

        self._info_nine_box_potential.setText(nine_box_potential)
        self._info_nine_box_performance.setText(nine_box_performance)
        self._nine_box_org_widget.set_supervisor(top_level_supervisor)
        self._nine_box_org_widget.setVisible(manager)

        rating = "None"
        if "Ratings" in p.keys():
            rating = str(p["Ratings"][-1]["Rating"])

        self._info_rating.setText(rating)
        self._rating_org_widget.set_supervisor(top_level_supervisor)
        self._rating_org_widget.setVisible(manager)

        salary = "N/A"
        salary_usd = "N/A"
        if "Salaries" in p.keys():
            salary_val = p["Salaries"][-1]["Salary"]
            salary = str(salary_val)
            salary_usd_val = salary_val * fx_rates[p["Locations"][-1]["Location"]]
            salary_usd = str(int(salary_usd_val))

        rollup_salary_usd = "N/A"
        rollup_salary_usd_val = int(self._people[top_level_supervisor]["Rollup Salaries"])

        if manager:
            rollup_missing_salaries = self._people[top_level_supervisor]["Missing Salaries"]
            rollup_salary_usd = str("{:d} (Missing {:d} people)").format(rollup_salary_usd_val, rollup_missing_salaries)

        self._info_salary.setText(salary)
        self._info_salary_usd.setText(salary_usd)
        self._info_rollup_salary_usd.setText(rollup_salary_usd)
        self._salary_org_widget.set_supervisor(top_level_supervisor)
        self._salary_org_widget.setVisible(manager)

        self.update()


def scan_org_tree(people, supervisor_uen, depth):
    # Scan each direct report recursively, computing how deep each person is in
    # the overall org, and how many reports roll up to them in total.
    num_reports = 0
    rollup_salaries = 0
    missing_salaries = 0
    p = people[supervisor_uen]
    for i in p["Direct Reports"]:
        (nr, rs, ms) = scan_org_tree(people, i, depth + 1)
        num_reports += nr
        rollup_salaries += rs
        missing_salaries += ms

    p["Org Depth"] = depth
    p["Total Reports"] = num_reports
    p["Rollup Salaries"] = rollup_salaries
    p["Missing Salaries"] = missing_salaries

    # Scan each direct report, but this time compute the fraction of the overall
    # team their subteam represents.
    for i in p["Direct Reports"]:
        people[i]["Supervisor Fraction"] = (people[i]["Total Reports"] + 1) / num_reports

    # Sort the direct reports to put the one with the largest fraction of the org first.
    drs = p["Direct Reports"]
    for i in range(len(drs)):
        for j in range(len(drs) - i - 1):
            if people[drs[j]]["Supervisor Fraction"] < people[drs[j + 1]]["Supervisor Fraction"]:
                t = drs[j + 1]
                drs[j + 1] = drs[j]
                drs[j] = t

    start_date = p["Person"]["Start Date"]
    t = time.strptime(start_date, "%Y-%m-%d")
    ot = time.strptime("2016-01-01", "%Y-%m-%d")
    cur_time = time.time()
    org_elapsed_time = cur_time - time.mktime(ot)
    worked_time = cur_time - time.mktime(t)
    p["Service Duration"] = cur_time - time.mktime(t)
    p["Service Duration Fraction"] = worked_time / org_elapsed_time

    num_reports += 1
    if "Salaries" not in p["Person"].keys():
        missing_salaries += 1
    else:
        salary = p["Person"]["Salaries"][-1]["Salary"]
        salary_usd = salary * fx_rates[p["Person"]["Locations"][-1]["Location"]]
        rollup_salaries += salary_usd

    return (num_reports, rollup_salaries, missing_salaries)

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

fail, all_people, top_level_supervisor = scan_json(json_data)
if fail:
    exit()

scan_org_tree(all_people, top_level_supervisor, 0)
all_people[top_level_supervisor]["Supervisor Fraction"] = 1

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.set_people(all_people, top_level_supervisor)
window.show()
app.exec()
