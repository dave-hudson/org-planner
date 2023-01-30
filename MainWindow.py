from PySide6 import QtGui, QtWidgets, QtCore
from ColourKey1DWidget import ColourKey1DWidget
from ColourKey2DWidget import ColourKey2DWidget
from PeopleListWidget import PeopleListWidget
from PeopleTreeWidget import PeopleTreeWidget
from PeopleSelectorWidget import PeopleSelectorWidget
from PersonWidget import PersonWidget
from MainSplitter import MainSplitter
from HLine import HLine
from SunburstOrgWidget import fx_rates
from SunburstOrgKeyWidget import SunburstOrgKeyWidget
from GenderInfoWidget import GenderInfoWidget, gender_colours
from GradeInfoWidget import GradeInfoWidget, grade_colours
from LocationInfoWidget import LocationInfoWidget, location_colours
from NumDirectReportsInfoWidget import NumDirectReportsInfoWidget, num_direct_reports_colours
from NineBoxSunburstOrgWidget import NineBoxSunburstOrgWidget, nine_box_colours
from RatingSunburstOrgWidget import RatingSunburstOrgWidget, rating_colours
from RollupSalarySunburstOrgWidget import RollupSalarySunburstOrgWidget, rollup_salary_colours
from SalarySunburstOrgWidget import SalarySunburstOrgWidget, salary_colours
from SalaryOffsetSunburstOrgWidget import SalaryOffsetSunburstOrgWidget, salary_offset_colours, salary_offset_labels
from SalaryBandOffsetSunburstOrgWidget import SalaryBandOffsetSunburstOrgWidget, salary_band_offset_colours
from ServiceDurationInfoWidget import ServiceDurationInfoWidget, service_duration_colours
from TeamInfoWidget import TeamInfoWidget, team_colours
from TypeSunburstOrgWidget import TypeSunburstOrgWidget, type_colours

# This is the QSS used to ensure the app renders correctly.  It's parameterized
# using string.format() form so dark and light mode parameters can be provided,
# but doing this means there's only one QSS to maintain.
qss = """
QWidget {{
    background-color: {};
    color: {};
    font-family: "Verdana";
    border-style: solid;
    border-width: 0px;
}}

QMenuBar {{
    background-color: {};
    padding: 4px;
}}

QMenuBar::item {{
    border-radius: 4px;
    padding: 4px;
}}

QMenuBar::item:selected {{
    background-color: {};
}}

QMenu {{
    background-color: {};
    border-color: {};
    border-width: 1px;
    border-style: solid;
    border-radius: 4px;
}}

QMenu::item {{
    margin: 3px 5px;
    padding: 4px 4px 4px 10px;
}}

QMenu::item:selected {{
    background-color: {};
    border-radius: 4px;
}}

QListWidget::item {{
    padding: 4px;
}}

QTreeWidget::item {{
    padding: 4px;
}}

QScrollBar {{
    background: {};
}}

/*
 * We don't want the arrows on scroll bars.
 */
QScrollBar::add-line {{
    height: 0px;
}}

QScrollBar::sub-line {{
    height: 0px;
}}

QScrollBar::add-page {{
    background: none;
}}

QScrollBar::sub-page {{
    background: none;
}}

QScrollBar::handle {{
    background: {};
}}

ColourBoxWidget {{
    border-top: 1px solid #808080;
    border-left: 1px solid #808080;
}}

ColourBoxLabelWidget {{
    background-color: {};
    color: {};
    border-top: 1px solid #808080;
    border-left: 1px solid #808080;
}}

ColourKey1DWidget {{
    border-right: 1px solid #808080;
    border-bottom: 1px solid #808080;
}}

ColourKey2DWidget {{
    border-right: 1px solid #808080;
    border-bottom: 1px solid #808080;
}}

HLine {{
    max-height: 0;
    border-top: 1px;
    border-style: solid;
    border-color: {};
}}

PeopleListWidget {{
    padding: 4px;
    background-color: {};
}}

PeopleTreeWidget {{
    padding: 4px;
    background-color: {};
}}

MainSplitter::handle {{
    width: 1px;
    background-color: {};
}}
"""

dark_qss_config = [
    "#202020",
    "white",
    "#353535",
    "#484848",
    "#353535",
    "#808080",
    "#6060c0",
    "#505050",
    "#808080",
    "#404040",
    "white",
    "white",
    "#303030",
    "#303030",
    "#c0c0c0"
]

light_qss_config = [
    "#f8f8f8",
    "black",
    "#c0c0c0",
    "#d8d8d8",
    "#f8f8f8",
    "#808080",
    "#6060c0",
    "#b0b0b0",
    "#808080",
    "#c0c0c0",
    "black",
    "black",
    "#d8d8d8",
    "#d8d8d8",
    "#404040"
]

class MainWindow(QtWidgets.QMainWindow):
    """
    The main window class for the application.
    """
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Org Planner")
        self._locations = {}
        self._people = {}
        self._uen = 0

        self._dark_mode = True
        self._dark_mode_action = QtGui.QAction("&Dark Mode", self)
        self._dark_mode_action.setCheckable(True)
        self._dark_mode_action.setChecked(True)
        self._dark_mode_action.triggered.connect(self._dark_mode_triggered)
        self._set_app_palette()

        self._hide_sensitive_data = True
        self._hide_sensitive_data_action = QtGui.QAction("&Hide Sensitive Data", self)
        self._hide_sensitive_data_action.setCheckable(True)
        self._hide_sensitive_data_action.setChecked(True)
        self._hide_sensitive_data_action.triggered.connect(self._hide_sensitive_data_triggered)

        self._view_type = 0
        self._list_view_action = QtGui.QAction("&List View", self)
        self._list_view_action.setCheckable(True)
        self._list_view_action.setChecked(True)
        self._list_view_action.triggered.connect(self._list_view_triggered)
        self._tree_view_action = QtGui.QAction("&Tree View", self)
        self._tree_view_action.setCheckable(True)
        self._tree_view_action.setChecked(False)
        self._tree_view_action.triggered.connect(self._tree_view_triggered)

        # Create a menu bar and menu drop-downs.
        self._menu_bar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self._menu_bar)
        view_menu = self._menu_bar.addMenu("&View")
        view_menu.addAction(self._dark_mode_action)
        view_menu.addSeparator()
        view_menu.addAction(self._hide_sensitive_data_action)
        view_menu.addSeparator()
        view_menu.addAction(self._list_view_action)
        view_menu.addAction(self._tree_view_action)
        view_menu.addSeparator()
        view_menu.setWindowFlags(view_menu.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.NoDropShadowWindowHint)
        view_menu.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._people_list_widget = PeopleListWidget(self)
        self._people_list_widget.currentItemChanged.connect(self._people_list_index_changed)
        self._people_list_widget.setFocus()
        self._people_tree_widget = PeopleTreeWidget(self)
        self._people_tree_widget.currentItemChanged.connect(self._people_tree_item_changed)
        self._people_tree_widget.setHeaderHidden(True)
        self._people_tree_widget.setHidden(True)
        people_selector_widget = PeopleSelectorWidget(self, self._people_list_widget, self._people_tree_widget)

        self._side_layout = QtWidgets.QVBoxLayout()
        self._side_layout.setSpacing(12)

        heading_font = QtGui.QFont()
        heading_font.setBold(True)
        heading_font.setPointSize(heading_font.pointSize() * 2)

        self._info_name = QtWidgets.QLabel("")
        self._info_name.setFont(heading_font)
        self._side_layout.addWidget(self._info_name)
        self._side_layout.addWidget(QtWidgets.QLabel(""))

        self._info_uen = self._add_info_text("UEN")
        self._info_supervisor_uen = self._add_info_text("Supervisor UEN")

        self._side_layout.addWidget(HLine())
        self._num_direct_reports_info = NumDirectReportsInfoWidget()
        self._side_layout.addWidget(self._num_direct_reports_info)

        self._side_layout.addWidget(HLine())
        self._team_info = TeamInfoWidget()
        self._side_layout.addWidget(self._team_info)

        self._side_layout.addWidget(HLine())
        self._info_type = self._add_info_text("Type")
        self._type_org_widget = SunburstOrgKeyWidget(TypeSunburstOrgWidget(), ColourKey1DWidget(type_colours, "Type Counts"))
        self._side_layout.addWidget(self._type_org_widget)

        self._side_layout.addWidget(HLine())
        self._location_info = LocationInfoWidget()
        self._side_layout.addWidget(self._location_info)

        self._side_layout.addWidget(HLine())
        self._grade_info = GradeInfoWidget()
        self._side_layout.addWidget(self._grade_info)

        self._side_layout.addWidget(HLine())
        self._gender_info = GenderInfoWidget()
        self._side_layout.addWidget(self._gender_info)

        self._side_layout.addWidget(HLine())
        self._service_duration_info = ServiceDurationInfoWidget()
        self._side_layout.addWidget(self._service_duration_info)

        self._side_layout.addWidget(HLine())
        self._info_nine_box_potential = self._add_info_text("9-box Grid Potential")
        self._info_nine_box_performance = self._add_info_text("9-box Grid Performance")
        self._nine_box_org_widget = SunburstOrgKeyWidget(NineBoxSunburstOrgWidget(), ColourKey2DWidget(nine_box_colours, "9 Box Counts"))
        self._side_layout.addWidget(self._nine_box_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_rating = self._add_info_text("Rating")
        self._rating_org_widget = SunburstOrgKeyWidget(RatingSunburstOrgWidget(), ColourKey1DWidget(rating_colours, "Rating Counts"))
        self._side_layout.addWidget(self._rating_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_salary = self._add_info_text("Salary")
        self._info_salary_usd = self._add_info_text("Salary (USD)")
        self._salary_org_widget = SunburstOrgKeyWidget(SalarySunburstOrgWidget(), ColourKey1DWidget(salary_colours, "Salary Counts"))
        self._side_layout.addWidget(self._salary_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_salary_offset = self._add_info_text("Mid-band Salary Offset")
        self._info_salary_offset_usd = self._add_info_text("Mid-band Salary Offset (USD)")
        self._info_salary_offset_percentage = self._add_info_text("Mid-band Salary Offset (%)")
        salary_offset_legend = ColourKey1DWidget(salary_offset_colours, "Salary Offset Counts")
        salary_offset_legend.set_labels(salary_offset_labels)
        self._salary_offset_org_widget = SunburstOrgKeyWidget(SalaryOffsetSunburstOrgWidget(), salary_offset_legend)
        self._side_layout.addWidget(self._salary_offset_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_salary_band_lower_limit = self._add_info_text("Salary Band Lower Limit")
        self._info_salary_band_salary = self._add_info_text("Salary")
        self._info_salary_band_upper_limit = self._add_info_text("Salary Band Upper Limit")
        self._info_salary_band_offset = self._add_info_text("Salary Comparison With Band")
        salary_band_offset_legend = ColourKey1DWidget(salary_band_offset_colours)
        self._salary_band_offset_org_widget = SunburstOrgKeyWidget(SalaryBandOffsetSunburstOrgWidget(), salary_band_offset_legend)
        self._side_layout.addWidget(self._salary_band_offset_org_widget)

        self._side_layout.addWidget(HLine())
        self._info_rollup_salary_usd = self._add_info_text("Rollup Salary (USD)")
        self._rollup_salary_org_widget = SunburstOrgKeyWidget(RollupSalarySunburstOrgWidget(), ColourKey1DWidget(rollup_salary_colours))
        self._side_layout.addWidget(self._rollup_salary_org_widget)

        # Insert a spacer so the layout engine doesn't try to spread out the
        # info panel elements if they take less space than the visible
        # window.
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        self._side_layout.addItem(spacer)

        widget = PersonWidget(self)
        widget.setLayout(self._side_layout)

        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidget(widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        splitter_widget = MainSplitter(self)
        splitter_widget.addWidget(people_selector_widget)
        splitter_widget.addWidget(scroll_area)
        splitter_widget.setStretchFactor(0, 1)
        splitter_widget.setStretchFactor(1, 3)

        self.setCentralWidget(splitter_widget)

        self._set_redacted(self._hide_sensitive_data)

    def _add_info_text(self, text):
        info_layout = QtWidgets.QGridLayout()
        self._side_layout.addLayout(info_layout)
        info_layout.addWidget(QtWidgets.QLabel(text), 0, 0, 1, 1)
        info_widget = QtWidgets.QLabel("")
        info_layout.addWidget(info_widget, 0, 1, 1, 4)
        return info_widget

    def _set_app_palette(self):
        if (self._dark_mode):
            self.setStyleSheet(qss.format(*dark_qss_config))
        else:
            self.setStyleSheet(qss.format(*light_qss_config))

    def _dark_mode_triggered(self, s):
        """
        Called when the "Dark Mode" menu item is triggered.
        """

        self._dark_mode = not self._dark_mode
        self._dark_mode_action.setChecked(self._dark_mode)
        self._set_app_palette()

    def _hide_sensitive_data_triggered(self, s):
        """
        Called when the "Hide Sensitive Data" menu item is triggered.
        """

        self._hide_sensitive_data = not self._hide_sensitive_data
        self._hide_sensitive_data_action.setChecked(self._hide_sensitive_data)
        self._set_redacted(self._hide_sensitive_data)

    def _list_view_triggered(self, s):
        """
        Called when the "List View" menu item is triggered.

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

    def _tree_view_triggered(self, s):
        """
        Called when the "Tree View" menu item is triggered.

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

    def set_locations(self, locations):
        self._locations = locations

        self._num_direct_reports_info.set_locations(locations)
        self._team_info.set_locations(locations)
        self._type_org_widget.set_locations(locations)
        self._location_info.set_locations(locations)
        self._grade_info.set_locations(locations)
        self._gender_info.set_locations(locations)
        self._service_duration_info.set_locations(locations)
        self._nine_box_org_widget.set_locations(locations)
        self._rating_org_widget.set_locations(locations)
        self._salary_org_widget.set_locations(locations)
        self._salary_offset_org_widget.set_locations(locations)
        self._salary_band_offset_org_widget.set_locations(locations)
        self._rollup_salary_org_widget.set_locations(locations)

        self.update()

    def set_people(self, people, supervisor_uen):
        self._people = people

        for i in people:
            self._people_list_widget.addItem(people[i]["Person"]["Name"])

        self._people_list_widget.sortItems(QtGui.Qt.AscendingOrder)

        top_level = QtWidgets.QTreeWidgetItem()
        top_level.setText(0, people[supervisor_uen]["Person"]["Name"])
        self._set_people_tree(supervisor_uen, top_level)
        self._people_tree_widget.insertTopLevelItem(0, top_level)
        self._people_tree_widget.expandAll()

        self._num_direct_reports_info.set_people(people)
        self._team_info.set_people(people)
        self._type_org_widget.set_people(people)
        self._location_info.set_people(people)
        self._grade_info.set_people(people)
        self._gender_info.set_people(people)
        self._service_duration_info.set_people(people)
        self._nine_box_org_widget.set_people(people)
        self._rating_org_widget.set_people(people)
        self._salary_org_widget.set_people(people)
        self._salary_offset_org_widget.set_people(people)
        self._salary_band_offset_org_widget.set_people(people)
        self._rollup_salary_org_widget.set_people(people)

        list_selected = self._people_list_widget.item(0)
        self._people_list_widget.setCurrentItem(list_selected)

        self.update()

    def set_uen(self, uen):
        self._uen = uen
        self._num_direct_reports_info.set_uen(uen)
        self._team_info.set_uen(uen)
        self._location_info.set_uen(uen)
        self._grade_info.set_uen(uen)
        self._gender_info.set_uen(uen)
        self._service_duration_info.set_uen(uen)
        self._render_uen()

    def _render_uen(self):
        uen = self._uen
        if uen == 0:
            return

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

        self._num_direct_reports_info.render_uen()
        self._team_info.render_uen()

        self._info_type.setText(p["Type"])
        self._type_org_widget.set_uen(uen, is_manager)

        self._location_info.render_uen()
        self._grade_info.render_uen()
        self._gender_info.render_uen()
        self._service_duration_info.render_uen()

        nine_box_potential = "None"
        nine_box_performance = "None"
        if self._hide_sensitive_data:
            nine_box_potential = "Hidden"
            nine_box_performance = "Hidden"
        else:
            if "9 Box" in p.keys():
                nine_box_potential = p["9 Box"][-1]["Potential"]
                nine_box_performance = p["9 Box"][-1]["Performance"]

        self._info_nine_box_potential.setText(nine_box_potential)
        self._info_nine_box_performance.setText(nine_box_performance)
        self._nine_box_org_widget.set_uen(uen, is_manager)

        rating = "None"
        if self._hide_sensitive_data:
            rating = "Hidden"
        else:
            if "Ratings" in p.keys():
                rating = str(p["Ratings"][-1]["Rating"])

        self._info_rating.setText(rating)
        self._rating_org_widget.set_uen(uen, is_manager)

        salary = "N/A"
        salary_usd = "N/A"
        if self._hide_sensitive_data:
            salary = "Hidden"
            salary_usd = "Hidden"
        else:
            if "Salaries" in p.keys():
                salary_val = p["Salaries"][-1]["Salary"]
                salary = str(salary_val)
                salary_usd_val = salary_val * fx_rates[p["Locations"][-1]["Location"]]
                salary_usd = str(int(salary_usd_val))

        self._info_salary.setText(salary)
        self._info_salary_usd.setText(salary_usd)
        self._salary_org_widget.set_uen(uen, is_manager)

        salary_offset = "N/A"
        salary_offset_usd = "N/A"
        salary_offset_percentage = "N/A"
        if self._hide_sensitive_data:
            salary_offset = "Hidden"
            salary_offset_usd = "Hidden"
            salary_offset_percentage = "Hidden"
        else:
            if "Salary Offset" in self._people[uen].keys():
                salary_offset = str(self._people[uen]["Salary Offset"])
                salary_offset_usd = str(int(self._people[uen]["Salary Offset USD"]))
                salary_offset_percentage = "{:.1f}%".format(self._people[uen]["Salary Offset Percentage"])

        self._info_salary_offset.setText(salary_offset)
        self._info_salary_offset_usd.setText(salary_offset_usd)
        self._info_salary_offset_percentage.setText(salary_offset_percentage)
        self._salary_offset_org_widget.set_uen(uen, is_manager)

        salary_band_lower_limit = "N/A"
        salary_band_upper_limit = "N/A"
        salary_band_offset = "N/A"
        if self._hide_sensitive_data:
            salary_band_lower_limit = "Hidden"
            salary_band_upper_limit = "Hidden"
            salary_band_offset = "Hidden"
        else:
            if "Salary Band Offset" in self._people[uen].keys():
                salary_band_lower_limit = self._people[uen]["Salary Band Lower Limit"]
                salary_band_upper_limit = self._people[uen]["Salary Band Upper Limit"]
                salary_band_offset = str(self._people[uen]["Salary Band Offset"])

        self._info_salary_band_lower_limit.setText(str(salary_band_lower_limit))
        self._info_salary_band_salary.setText(salary)
        self._info_salary_band_upper_limit.setText(str(salary_band_upper_limit))
        self._info_salary_band_offset.setText(salary_band_offset)
        self._salary_band_offset_org_widget.set_uen(uen, is_manager)

        rollup_salary_usd = "N/A"
        rollup_salary_usd_val = int(self._people[uen]["Rollup Salaries"])
        if self._hide_sensitive_data:
            rollup_salary_usd = "Hidden"
        else:
            if is_manager:
                rollup_missing_salaries = self._people[uen]["Missing Salaries"]
                ppl = "People"
                if rollup_missing_salaries == 1:
                    ppl = "Person"

                rollup_salary_usd = str("{} (Missing {:d} {})").format(rollup_salary_usd_val, rollup_missing_salaries, ppl)

        self._info_rollup_salary_usd.setText(rollup_salary_usd)
        self._rollup_salary_org_widget.set_uen(uen, is_manager)

        self.update()

    def _set_redacted(self, is_redacted):
        vis = not is_redacted

        self._rating_org_widget.set_redacted(is_redacted)
        self._nine_box_org_widget.set_redacted(is_redacted)
        self._salary_org_widget.set_redacted(is_redacted)
        self._salary_offset_org_widget.set_redacted(is_redacted)
        self._salary_band_offset_org_widget.set_redacted(is_redacted)
        self._rollup_salary_org_widget.set_redacted(is_redacted)

        self._render_uen()
