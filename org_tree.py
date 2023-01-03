import json
import sys
from PySide6 import QtCore, QtGui, QtWidgets

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

    return num_reports

class SpiralOrgWidget(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.people = {}
        self.top_level_supervisor = 0

    def setPeople(self, people, top_level_supervisor):
        self.people = people
        self.top_level_supervisor = top_level_supervisor

        # Work out how many layers deep the org goes.
        level_count = [0] * 10
        for i in people:
            p = people[i]
            depth = p["Org Depth"]
            level_count[depth] += 1

        self.max_depth = 0
        for j in range((len(level_count) - 1), -1, -1):
            if level_count[j] != 0:
                self.max_depth = j
                break

        self.max_radius = 480
        self.spacing = 20
        self.ring_width = self.max_radius / (self.max_depth + 1)

        self.setMinimumSize(2 * (self.spacing + self.max_radius),
                            2 * (self.spacing + self.max_radius))
        self.update()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.RenderHints.Antialiasing)
        self.drawWidget(qp)
        qp.end()

    def recurseDrawWidget(self, painter, supervisor_uen, depth, start_angle, start_arc):
        supervisor_person = self.people[supervisor_uen]

        angle = start_angle
        for i in supervisor_person["Direct Reports"]:
            radius = (depth + 1) * self.ring_width
            brush = QtGui.QBrush("lightgray")
            painter.setBrush(brush)
            arc = self.people[i]["Supervisor Fraction"] * start_arc
            self.recurseDrawWidget(painter, i, depth + 1, angle, arc)
            painter.drawPie(self.spacing + self.max_radius - radius,
                            self.spacing + self.max_radius - radius,
                            radius * 2, radius * 2,
                            angle * 16, arc * 16)
            angle += arc

    def drawWidget(self, painter):
        if len(self.people) == 0:
            return

        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black, 1, QtCore.Qt.PenStyle.SolidLine)
        painter.setPen(pen)

        # Recursively draw the outer layers of the org chart.
        self.recurseDrawWidget(painter, top_level_supervisor, 1, 0, 360)

        # Then draw the inner-most node.
        painter.drawEllipse(self.spacing + self.max_radius - self.ring_width,
                            self.spacing + self.max_radius - self.ring_width,
                            self.ring_width * 2, self.ring_width * 2)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.org_widget = SpiralOrgWidget()
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidget(self.org_widget)
        self.scroll_area.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.setCentralWidget(self.scroll_area)

    def setPeople(self, people, top_level_supervisor):
        self.org_widget.setPeople(people, top_level_supervisor)
        self.update()


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
window.setPeople(all_people, top_level_supervisor)
window.show()
app.exec()
