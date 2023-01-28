from abc import abstractmethod
from PySide6 import QtGui, QtWidgets

fx_rates = {
    "UK": 1.33,
    "Ireland": 1.16,
    "India": 0.014,
    "Bulgaria": 1.16,
    "Singapore": 0.76,
    "USA": 1.0
}

class SunburstOrgWidget(QtWidgets.QWidget):
    """
    A widget base class used to draw sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()
        self._locations = {}
        self._people = {}
        self._uen = 0

    def _scan_depth(self, supervisor):
        org_depth = self._people[supervisor]["Org Depth"]
        for i in self._people[supervisor]["Direct Reports"]:
            d = self._scan_depth(i)
            if d > org_depth:
                org_depth = d

        return org_depth

    @abstractmethod
    def _get_brush_colour(self, uen):
        pass

    def _setup_brush(self, painter, uen):
        colours = self._get_brush_colour(uen)
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

    def set_locations(self, locations):
        self._locations = locations

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
