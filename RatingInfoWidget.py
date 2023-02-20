from InfoOrgKeyWidget import InfoOrgKeyWidget
from RatingColourKey1DWidget import RatingColourKey1DWidget
from RatingSunburstOrgWidget import RatingSunburstOrgWidget, rating_colours
from SunburstOrgKeyWidget import SunburstOrgKeyWidget

class RatingInfoWidget(InfoOrgKeyWidget):
    """
    A widget class used to display performance rating information.
    """
    def __init__(self) -> None:
        super().__init__()

        self._hide_sensitive_data = True

        self._info_rating = self._add_info_text("Rating")
        legend = RatingColourKey1DWidget(rating_colours)
        self._org_widget = SunburstOrgKeyWidget(RatingSunburstOrgWidget(), legend)
        self._layout.addWidget(self._org_widget)
        self._org_widget.person_clicked.connect(self._person_clicked)

    def update_contents(self):
        uen = self._uen
        is_manager = self._is_manager
        p = self._people[uen]

        rating = "None"
        if self._hide_sensitive_data:
            rating = "Hidden"
        else:
            if "Ratings" in p.keys():
                rating = str(p["Ratings"][-1]["Rating"])

        self._info_rating.setText(rating)
        self._org_widget.set_uen(uen, is_manager)

    def set_redacted(self, is_redacted):
        self._hide_sensitive_data = is_redacted
        self._org_widget.set_redacted(is_redacted)
