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

class HLine(QtWidgets.QFrame):
    """
    A widget class used to insert horizontal dividers between other widgets.
    """
    def __init__(self):
        super(HLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class ColourBoxWidget(QtWidgets.QLabel):
    def __init__(self, text, colour) -> None:
        super().__init__(text)
        self.setAutoFillBackground(True)
        self.setMargin(4)

        palette = self.palette()
        c = QtGui.QColor(colour[0], colour[1], colour[2], 0xff)
        palette.setColor(QtGui.QPalette.Window, c)
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

            right_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self._layout.addItem(right_spacer, row, 2)

            row += 1

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
            print(cdi)
            label_widget = ColourBoxWidget(cdi, [0x20, 0x20, 0x20])
            self._layout.addWidget(label_widget, row, 0)

            col = 1
            for cdj in colour_dict[cdi]:
                colour_widget = ColourBoxWidget("", colour_dict[cdi][cdj])
                self._layout.addWidget(colour_widget, row, col)

                col += 1

            right_spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            self._layout.addItem(right_spacer, row, col)

            row += 1

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
        colours = [0xc0, 0xc0, 0xc0]

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
            if "Start Date" in p["Person"].keys():
                start_date = p["Person"]["Start Date"]
                t = time.strptime(start_date, "%Y-%m-%d")
                ot = time.strptime("2016-01-01", "%Y-%m-%d")
                cur_time = time.time()
                org_elapsed_time = cur_time - time.mktime(ot)
                worked_time = cur_time - time.mktime(t)
                worked_fraction = worked_time / org_elapsed_time
                base_colour = int(0xc0 * worked_fraction)
                colours = [0xff, 0xff - base_colour, 0xff - base_colour, 0xff]
        else:
            if "9 Box" in p["Person"].keys():
                nine_box_potential = p["Person"]["9 Box"][-1]["Potential"]
                nine_box_performance = p["Person"]["9 Box"][-1]["Performance"]
                if nine_box_potential in nine_box_colours:
                    potential_colours = nine_box_colours[nine_box_potential]
                    if nine_box_performance in potential_colours:
                        colours = potential_colours[nine_box_performance]

        brush = QtGui.QBrush(QtGui.QColor(colours[0], colours[1], colours[2], 0xff))
        painter.setBrush(brush)

    def _recurse_draw_widget(self, painter, supervisor_uen, depth, start_angle, start_arc):
        supervisor_person = self._people[supervisor_uen]

        angle = start_angle
        for i in supervisor_person["Direct Reports"]:
            radius = (depth + 1) * self._ring_width
            p = self._people[i]
            arc = p["Supervisor Fraction"] * start_arc
            self._recurse_draw_widget(painter, i, depth + 1, angle, arc)
            self._setup_brush(painter, i)
            painter.drawPie(self._spacing + self._max_radius - radius,
                            self._spacing + self._max_radius - radius,
                            radius * 2, radius * 2,
                            angle * 16, arc * 16)
            angle += arc

    def _draw_widget(self, painter):
        if len(self._people) == 0:
            return

        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 1, QtCore.Qt.PenStyle.SolidLine)
        painter.setPen(pen)

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
        self._render_type = r;
        self.update()

    def set_people(self, people, top_level_supervisor):
        self._people = people
        self._top_level_supervisor = top_level_supervisor

        supervisor_org_depth = people[top_level_supervisor]["Org Depth"]

        # Work out how many layers deep the org goes.
        self._max_depth = self._scan_depth(top_level_supervisor)
        self._max_radius = 480
        self._spacing = 20
        self._ring_width = self._max_radius / (self._max_depth - supervisor_org_depth + 1)

        self.setMinimumSize(2 * (self._spacing + self._max_radius),
                            2 * (self._spacing + self._max_radius))
        self.update()

class MainWindow(QtWidgets.QMainWindow):
    """
    The main window class for the application.
    """
    def __init__(self) -> None:
        super().__init__()

        side_layout = QtWidgets.QVBoxLayout()

        location_text = QtWidgets.QLabel("Locations")
        side_layout.addWidget(location_text)
        self._location_org_widget = SunburstOrgWidget(0)
        side_layout.addWidget(self._location_org_widget)
        location_key_widget = ColourKey1DWidget(location_colours)
        side_layout.addWidget(location_key_widget)
        separator1 = HLine()
        side_layout.addWidget(separator1)

        grade_text = QtWidgets.QLabel("Grades")
        side_layout.addWidget(grade_text)
        self._grade_org_widget = SunburstOrgWidget(1)
        side_layout.addWidget(self._grade_org_widget)
        grade_key_widget = ColourKey1DWidget(grade_colours)
        side_layout.addWidget(grade_key_widget)
        separator2 = HLine()
        side_layout.addWidget(separator2)

        gender_text = QtWidgets.QLabel("Gender")
        side_layout.addWidget(gender_text)
        self._gender_org_widget = SunburstOrgWidget(2)
        side_layout.addWidget(self._gender_org_widget)
        gender_key_widget = ColourKey1DWidget(gender_colours)
        side_layout.addWidget(gender_key_widget)
        separator3 = HLine()
        side_layout.addWidget(separator3)

        service_duration_text = QtWidgets.QLabel("Service Duration")
        side_layout.addWidget(service_duration_text)
        self._service_duration_org_widget = SunburstOrgWidget(3)
        side_layout.addWidget(self._service_duration_org_widget)
        separator4 = HLine()
        side_layout.addWidget(separator4)

        nine_box_text = QtWidgets.QLabel("Latest 9-box Grid Ratings")
        side_layout.addWidget(nine_box_text)
        self._nine_box_org_widget = SunburstOrgWidget(4)
        side_layout.addWidget(self._nine_box_org_widget)
        nine_box_key_widget = ColourKey2DWidget(nine_box_colours)
        side_layout.addWidget(nine_box_key_widget)

        widget = QtWidgets.QWidget()
        widget.setLayout(side_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setCentralWidget(scroll_area)

    def set_people(self, people, top_level_supervisor):
        self._location_org_widget.set_people(people, top_level_supervisor)
        self._grade_org_widget.set_people(people, top_level_supervisor)
        self._gender_org_widget.set_people(people, top_level_supervisor)
        self._nine_box_org_widget.set_people(people, top_level_supervisor)
        self._service_duration_org_widget.set_people(people, top_level_supervisor)
        self.update()

def scan_org_tree(people, supervisor_uen, depth):
    # Scan each direct report recursively, computing how deep each person is in
    # the overall org, and how many reports roll up to them in total.
    num_reports = 0
    p = people[supervisor_uen]
    for i in p["Direct Reports"]:
        num_reports += scan_org_tree(people, i, depth + 1) + 1

    p["Org Depth"] = depth
    p["Total Reports"] = num_reports

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

    return num_reports

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
