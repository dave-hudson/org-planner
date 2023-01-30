from SunburstOrgWidget import SunburstOrgWidget

salary_band_offset_colours = {
    "Below": [0x30, 0x30, 0xf0],
    "Within": [0x30, 0xf0, 0x30],
    "Above": [0xf0, 0x30, 0x30]
}

class SalaryBandOffsetSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw salary band analysis sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Salary Band Offset" in p.keys():
            salary_band_offset = p["Salary Band Offset"]
            colours = salary_band_offset_colours[str(salary_band_offset)]

        return colours
