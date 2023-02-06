from PySide6 import QtGui, QtWidgets, QtCore
from PeopleListWidget import PeopleListWidget
from PeopleTreeWidget import PeopleTreeWidget
from PeopleSelectorWidget import PeopleSelectorWidget
from PersonWidget import PersonWidget
from MainSplitter import MainSplitter
from HLine import HLine
from GenderInfoWidget import GenderInfoWidget
from GeneralInfoWidget import GeneralInfoWidget
from GradeInfoWidget import GradeInfoWidget
from LocationInfoWidget import LocationInfoWidget
from NumDirectReportsInfoWidget import NumDirectReportsInfoWidget
from NineBoxInfoWidget import NineBoxInfoWidget
from RatingInfoWidget import RatingInfoWidget
from RollupSalaryInfoWidget import RollupSalaryInfoWidget
from SalaryInfoWidget import SalaryInfoWidget
from SalaryOffsetInfoWidget import SalaryOffsetInfoWidget
from SalaryBandOffsetInfoWidget import SalaryBandOffsetInfoWidget
from ServiceDurationInfoWidget import ServiceDurationInfoWidget
from TeamInfoWidget import TeamInfoWidget
from EmploymentInfoWidget import EmploymentInfoWidget

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
    padding: 4px 8px 4px 8px;
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
    padding: 4px 4px 4px 4px;
}}

QMenu::indicator {{
    width: 20px;
    height: 16px;
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

# Parameters applied to the QSS above to give a dark mode version of the UI.
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

# Parameters applied to the QSS above to give a light mode version of the UI.
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
        self._history_list = []
        self._history_index = -1

        # The dark mode action allows toggling between light mode and dark
        # mode in the UI.
        self._dark_mode = True
        self._dark_mode_action = QtGui.QAction("&Dark Mode", self)
        self._dark_mode_action.setCheckable(True)
        self._dark_mode_action.setChecked(True)
        self._dark_mode_action.triggered.connect(self._dark_mode_triggered)
        self._set_app_palette()

        # By default we hide certain sensitive data when the application
        # starts.  There is an action associated with this.
        self._hide_sensitive_data = True
        self._hide_sensitive_data_action = QtGui.QAction("&Hide Sensitive Data", self)
        self._hide_sensitive_data_action.setCheckable(True)
        self._hide_sensitive_data_action.setChecked(True)
        self._hide_sensitive_data_action.triggered.connect(self._hide_sensitive_data_triggered)

        # The application supports either a list view or a tree view of the
        # people in the organization.  We have 2 actions associated with this
        # and at any one time, only one of them can be checked.
        self._view_type = 0
        self._list_view_action = QtGui.QAction("&List View", self)
        self._list_view_action.setCheckable(True)
        self._list_view_action.setChecked(True)
        self._list_view_action.triggered.connect(self._list_view_triggered)
        self._tree_view_action = QtGui.QAction("&Tree View", self)
        self._tree_view_action.setCheckable(True)
        self._tree_view_action.setChecked(False)
        self._tree_view_action.triggered.connect(self._tree_view_triggered)

        # We want to be able to zoom in and out, so we have 3 actions
        # associated with that.
        self._zoom_factor = 1.0
        self._actual_size_action = QtGui.QAction("Actual Size", self)
        self._actual_size_action.setShortcut(QtGui.QKeySequence("CTRL+0"))
        self._actual_size_action.triggered.connect(self._actual_size_triggered)
        self._actual_size_action.setEnabled(False)
        self._zoom_in_action = QtGui.QAction("Zoom In", self)
        self._zoom_in_action.setShortcut(QtGui.QKeySequence("CTRL+="))
        self._zoom_in_action.triggered.connect(self._zoom_in_triggered)
        self._zoom_out_action = QtGui.QAction("Zoom Out", self)
        self._zoom_out_action.setShortcut(QtGui.QKeySequence("CTRL+-"))
        self._zoom_out_action.triggered.connect(self._zoom_out_triggered)

        # We want to allow a user to navigate back to a previous view, or
        # to go forwards again if they've already gone back.  We have 2
        # actions to achieive this, with keyboard shortcuts.  By default,
        # neither is enabled.
        self._back_action = QtGui.QAction("Back", self)
        self._back_action.setShortcut(QtGui.QKeySequence("CTRL+["))
        self._back_action.triggered.connect(self._back_triggered)
        self._back_action.setEnabled(False)
        self._forward_action = QtGui.QAction("Forward", self)
        self._forward_action.setShortcut(QtGui.QKeySequence("CTRL+]"))
        self._forward_action.triggered.connect(self._forward_triggered)
        self._forward_action.setEnabled(False)

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
        view_menu.addAction(self._actual_size_action)
        view_menu.addAction(self._zoom_in_action)
        view_menu.addAction(self._zoom_out_action)
        view_menu.setWindowFlags(
            view_menu.windowFlags()
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.NoDropShadowWindowHint
        )
        view_menu.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        history_menu = self._menu_bar.addMenu("&History")
        history_menu.addAction(self._back_action)
        history_menu.addAction(self._forward_action)
        history_menu.setWindowFlags(
            view_menu.windowFlags()
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.NoDropShadowWindowHint
        )
        history_menu.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._people_list_widget = PeopleListWidget(self)
        self._people_list_widget.currentItemChanged.connect(self._people_list_index_changed)
        self._people_list_widget.setFocus()
        self._people_tree_widget = PeopleTreeWidget(self)
        self._people_tree_widget.currentItemChanged.connect(self._people_tree_item_changed)
        self._people_tree_widget.setHeaderHidden(True)
        self._people_tree_widget.setHidden(True)
        people_selector_widget = PeopleSelectorWidget(
            self, self._people_list_widget, self._people_tree_widget
        )

        self._side_layout = QtWidgets.QVBoxLayout()
        self._side_layout.setSpacing(12)

        self._general_info = GeneralInfoWidget()
        self._side_layout.addWidget(self._general_info)
        self._general_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._num_direct_reports_info = NumDirectReportsInfoWidget()
        self._side_layout.addWidget(self._num_direct_reports_info)
        self._num_direct_reports_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._team_info = TeamInfoWidget()
        self._side_layout.addWidget(self._team_info)
        self._team_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._employment_info = EmploymentInfoWidget()
        self._side_layout.addWidget(self._employment_info)
        self._employment_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._location_info = LocationInfoWidget()
        self._side_layout.addWidget(self._location_info)
        self._location_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._grade_info = GradeInfoWidget()
        self._side_layout.addWidget(self._grade_info)
        self._grade_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._gender_info = GenderInfoWidget()
        self._side_layout.addWidget(self._gender_info)
        self._gender_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._service_duration_info = ServiceDurationInfoWidget()
        self._side_layout.addWidget(self._service_duration_info)
        self._service_duration_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._nine_box_info = NineBoxInfoWidget()
        self._side_layout.addWidget(self._nine_box_info)
        self._nine_box_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._rating_info = RatingInfoWidget()
        self._side_layout.addWidget(self._rating_info)
        self._rating_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._salary_info = SalaryInfoWidget()
        self._side_layout.addWidget(self._salary_info)
        self._salary_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._salary_offset_info = SalaryOffsetInfoWidget()
        self._side_layout.addWidget(self._salary_offset_info)
        self._salary_offset_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._salary_band_offset_info = SalaryBandOffsetInfoWidget()
        self._side_layout.addWidget(self._salary_band_offset_info)
        self._salary_band_offset_info.person_clicked.connect(self._person_clicked)

        self._side_layout.addWidget(HLine())

        self._rollup_salary_info = RollupSalaryInfoWidget()
        self._side_layout.addWidget(self._rollup_salary_info)
        self._rollup_salary_info.person_clicked.connect(self._person_clicked)

        # Insert a spacer so the layout engine doesn't try to spread out the
        # info panel elements if they take less space than the visible
        # window.
        spacer = QtWidgets.QSpacerItem(0, 0, QtWidgets.QSizePolicy.Fixed,
                                       QtWidgets.QSizePolicy.MinimumExpanding)
        self._side_layout.addItem(spacer)

        widget = PersonWidget(self)
        widget.setLayout(self._side_layout)

        self._scroll_area = QtWidgets.QScrollArea(self)
        self._scroll_area.setWidget(widget)
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        splitter_widget = MainSplitter(self)
        splitter_widget.addWidget(people_selector_widget)
        splitter_widget.addWidget(self._scroll_area)
        splitter_widget.setStretchFactor(0, 1)
        splitter_widget.setStretchFactor(1, 3)

        self.setCentralWidget(splitter_widget)

        self._set_redacted(self._hide_sensitive_data)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        # If we have a back or forwards button press then do the relevant
        # back or forwards behaviour.
        if event.button() == QtCore.Qt.BackButton:
            event.accept()
            self._back_triggered(None)
            return

        if event.button() == QtCore.Qt.ForwardButton:
            event.accept()
            self._forward_triggered(None)
            return

    def _set_app_palette(self):
        # Set the QSS appropriately for the current light/dark mode setting.
        if self._dark_mode:
            self.setStyleSheet(qss.format(*dark_qss_config))
        else:
            self.setStyleSheet(qss.format(*light_qss_config))

    def _dark_mode_triggered(self, _):
        #  Called when the "Dark Mode" menu item is triggered.
        self._dark_mode = not self._dark_mode
        self._dark_mode_action.setChecked(self._dark_mode)
        self._set_app_palette()

    def _hide_sensitive_data_triggered(self, _):
        # Called when the "Hide Sensitive Data" menu item is triggered.
        self._hide_sensitive_data = not self._hide_sensitive_data
        self._hide_sensitive_data_action.setChecked(self._hide_sensitive_data)
        self._set_redacted(self._hide_sensitive_data)

    def _list_view_triggered(self, _):
        # Called when the "List View" menu item is triggered.
        #
        # We flip the application view type, flip the checkbox on the
        # list/tree view, hide the tree view and unhide the list view.
        self._view_type = 0
        self._list_view_action.setChecked(True)
        self._tree_view_action.setChecked(False)
        self._people_list_widget.setHidden(False)
        self._people_tree_widget.setHidden(True)

        # For UI continuity we take the current selected item from the tree
        # view and select the same entry in the list view.
        tree_selected = self._people_tree_widget.currentItem()
        item = self._people_list_widget.findItems(
            tree_selected.text(0), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive
        )
        self._people_list_widget.setCurrentItem(item[0])
        self._people_list_widget.setFocus()

    def _tree_view_triggered(self, _):
        # Called when the "Tree View" menu item is triggered.
        #
        # We flip the application view type, flip the checkbox on the
        # list/tree view, hide the list view and unhide the tree view.
        self._view_type = 1
        self._list_view_action.setChecked(False)
        self._tree_view_action.setChecked(True)
        self._people_list_widget.setHidden(True)
        self._people_tree_widget.setHidden(False)

        # For UI continuity we take the current selected item from the list
        # view and select the same entry in the tree view.
        list_selected = self._people_list_widget.currentItem()
        item = self._people_tree_widget.findItems(
            list_selected.text(), QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive
        )
        self._people_tree_widget.setCurrentItem(item[0])
        self._people_tree_widget.setFocus()

    def _actual_size_triggered(self, _):
        self._zoom_factor = 1.0
        self._actual_size_action.setEnabled(False)
        self._zoom_in_action.setEnabled(True)
        self._zoom_out_action.setEnabled(True)
        self._update_zoom()

    def _zoom_in_triggered(self, _):
        self._zoom_factor *= 1.189207
        if self._zoom_factor > 1.99:
            self._zoom_factor = 2
            self._zoom_in_action.setEnabled(False)

        self._actual_size_action.setEnabled(True)
        self._zoom_out_action.setEnabled(True)
        self._update_zoom()

    def _zoom_out_triggered(self, _):
        self._zoom_factor /= 1.189207
        if self._zoom_factor < 0.51:
            self._zoom_factor = 0.5
            self._zoom_out_action.setEnabled(False)

        self._actual_size_action.setEnabled(True)
        self._zoom_in_action.setEnabled(True)
        self._update_zoom()

    def _update_person(self, uen):
        # When we change the view of the currently active person we want
        # to ensure the tree and list views are updated to highlight them.
        name = self._people[uen]["Person"]["Name"]
        item = self._people_tree_widget.findItems(
            name, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive
        )
        self._people_tree_widget.setCurrentItem(item[0])
        self._people_tree_widget.setFocus()
        item = self._people_list_widget.findItems(
            name, QtCore.Qt.MatchExactly | QtCore.Qt.MatchRecursive
        )
        self._people_list_widget.setCurrentItem(item[0])
        self._people_list_widget.setFocus()

    def _set_scroll_position(self, scroll_pos):
        # When we move forwards and back, we'd like to have the scroll
        # position be the same as it was originally.  This method is
        # a timer callback that does this.
        self._scroll_area.verticalScrollBar().setValue(scroll_pos)

    def _forward_triggered(self, _):
        # Called when the "Forward" menu item is triggered.

        # If we're at the end of the history list then we can't go forwards.
        if self._history_index == (len(self._history_list) - 1):
            return

        self._back_action.setEnabled(True)
        self._history_index += 1
        if self._history_index == (len(self._history_list) - 1):
            self._forward_action.setEnabled(False)

        uen, scroll_pos = self._history_list[self._history_index]
        self.set_uen(uen)
        self._update_person(uen)
        QtCore.QTimer.singleShot(50, lambda: self._set_scroll_position(scroll_pos))

    def _back_triggered(self, _):
        # Called when the "Back" menu item is triggered.

        # If we're at the start of the history list then we can't go back.
        if self._history_index == 0:
            return

        self._forward_action.setEnabled(True)
        self._history_index -= 1
        if self._history_index == 0:
            self._back_action.setEnabled(False)

        uen, scroll_pos = self._history_list[self._history_index]
        self.set_uen(uen)
        self._update_person(uen)
        QtCore.QTimer.singleShot(50, lambda: self._set_scroll_position(scroll_pos))

    def _select_uen(self, uen):
        # When we select a new person we want to ensure we add them to the
        # viewing history.

        # If we've been asked to select the same person we're currently
        # viewing then do nothing.
        if uen == self._uen:
            return

        # If we've previously gone back and we're no longer at the end of the
        # history list then the new person that has been selected will
        # replace all people who are forward of the current position in the
        # history list.
        if self._history_index < (len(self._history_list) - 1):
            self._history_list = self._history_list[:self._history_index + 1]

        # If we've already recorded some history, we want to update the
        # top-most entry to reflect the current scroll bar position.  This
        # lets us go back to the same place when we go forwards and back.
        if self._history_index >= 0:
            scroll_pos = self._scroll_area.verticalScrollBar().value()
            uen_top, _ = self._history_list[-1]
            self._history_list[-1] = (uen_top, scroll_pos)
            self._back_action.setEnabled(True)

        t = (uen, 0)
        self._history_list.append(t)
        self._history_index += 1

        self.set_uen(uen)
        self._scroll_area.verticalScrollBar().setValue(0)

    def _person_clicked(self, uen):
        # Handler for propagating "person clicked" events from contained
        # widgets.
        self._select_uen(uen)
        self._update_person(uen)

    def _people_list_index_changed(self, list_item):
        # Handler for when a new person is selected in the list view.
        for i in self._people:
            if self._people[i]["Person"]["Name"] == list_item.text():
                self._select_uen(i)
                break

    def _people_tree_item_changed(self, tree_item):
        # Handler for when a new person is selected in the tree view.
        for i in self._people:
            if self._people[i]["Person"]["Name"] == tree_item.text(0):
                self._select_uen(i)
                break

    def set_locations(self, locations):
        self._locations = locations

        self._general_info.set_locations(locations)
        self._num_direct_reports_info.set_locations(locations)
        self._team_info.set_locations(locations)
        self._employment_info.set_locations(locations)
        self._location_info.set_locations(locations)
        self._grade_info.set_locations(locations)
        self._gender_info.set_locations(locations)
        self._service_duration_info.set_locations(locations)
        self._nine_box_info.set_locations(locations)
        self._rating_info.set_locations(locations)
        self._salary_info.set_locations(locations)
        self._salary_offset_info.set_locations(locations)
        self._salary_band_offset_info.set_locations(locations)
        self._rollup_salary_info.set_locations(locations)

        self.update()

    def _set_people_tree(self, supervisor_uen, supervisor_item):
        for p in self._people[supervisor_uen]["Direct Reports"]:
            twi = QtWidgets.QTreeWidgetItem()
            twi.setText(0, self._people[p]["Person"]["Name"])
            supervisor_item.addChild(twi)
            self._set_people_tree(p, twi)

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

        self._general_info.set_people(people, supervisor_uen)
        self._num_direct_reports_info.set_people(people, supervisor_uen)
        self._team_info.set_people(people, supervisor_uen)
        self._employment_info.set_people(people, supervisor_uen)
        self._location_info.set_people(people, supervisor_uen)
        self._grade_info.set_people(people, supervisor_uen)
        self._gender_info.set_people(people, supervisor_uen)
        self._service_duration_info.set_people(people, supervisor_uen)
        self._nine_box_info.set_people(people, supervisor_uen)
        self._rating_info.set_people(people, supervisor_uen)
        self._salary_info.set_people(people, supervisor_uen)
        self._salary_offset_info.set_people(people, supervisor_uen)
        self._salary_band_offset_info.set_people(people, supervisor_uen)
        self._rollup_salary_info.set_people(people, supervisor_uen)
        self._update_person(supervisor_uen)

        self.update()

    def set_uen(self, uen):
        self._uen = uen

        self._general_info.set_uen(uen)
        self._num_direct_reports_info.set_uen(uen)
        self._team_info.set_uen(uen)
        self._employment_info.set_uen(uen)
        self._location_info.set_uen(uen)
        self._grade_info.set_uen(uen)
        self._gender_info.set_uen(uen)
        self._service_duration_info.set_uen(uen)
        self._nine_box_info.set_uen(uen)
        self._rating_info.set_uen(uen)
        self._salary_info.set_uen(uen)
        self._salary_offset_info.set_uen(uen)
        self._salary_band_offset_info.set_uen(uen)
        self._rollup_salary_info.set_uen(uen)

        self._update_contents()

    def _update_contents(self):
        uen = self._uen
        if uen == 0:
            return

        self._general_info.update_contents()
        self._num_direct_reports_info.update_contents()
        self._team_info.update_contents()
        self._employment_info.update_contents()
        self._location_info.update_contents()
        self._grade_info.update_contents()
        self._gender_info.update_contents()
        self._service_duration_info.update_contents()
        self._nine_box_info.update_contents()
        self._rating_info.update_contents()
        self._salary_info.update_contents()
        self._salary_offset_info.update_contents()
        self._salary_band_offset_info.update_contents()
        self._rollup_salary_info.update_contents()

        self.update()

    def _update_zoom(self):
        uen = self._uen
        if uen == 0:
            return

        self._general_info.set_zoom(self._zoom_factor)
        self._num_direct_reports_info.set_zoom(self._zoom_factor)
        self._team_info.set_zoom(self._zoom_factor)
        self._employment_info.set_zoom(self._zoom_factor)
        self._location_info.set_zoom(self._zoom_factor)
        self._grade_info.set_zoom(self._zoom_factor)
        self._gender_info.set_zoom(self._zoom_factor)
        self._service_duration_info.set_zoom(self._zoom_factor)
        self._nine_box_info.set_zoom(self._zoom_factor)
        self._rating_info.set_zoom(self._zoom_factor)
        self._salary_info.set_zoom(self._zoom_factor)
        self._salary_offset_info.set_zoom(self._zoom_factor)
        self._salary_band_offset_info.set_zoom(self._zoom_factor)
        self._rollup_salary_info.set_zoom(self._zoom_factor)

        self.update()

    def _set_redacted(self, is_redacted):
        self._rating_info.set_redacted(is_redacted)
        self._nine_box_info.set_redacted(is_redacted)
        self._salary_info.set_redacted(is_redacted)
        self._salary_offset_info.set_redacted(is_redacted)
        self._salary_band_offset_info.set_redacted(is_redacted)
        self._rollup_salary_info.set_redacted(is_redacted)

        self._update_contents()
