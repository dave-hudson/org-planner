import math
from SunburstOrgWidget import SunburstOrgWidget

salary_offset_colours = {
    "-50000": [0x18, 0x3c, 0xb6],
    "-40000": [0x1e, 0x60, 0xb4],
    "-30000": [0x2d, 0x80, 0xb0],
    "-20000": [0x34, 0x9e, 0x60],
    "-10000": [0x40, 0xaf, 0x13],
    "0": [0x90, 0xc6, 0x12],
    "10000": [0xfd, 0xfa, 0x19],
    "20000": [0xf8, 0xc7, 0x10],
    "30000": [0xf6, 0x8d, 0x06],
    "40000": [0xf5, 0x61, 0x01],
    "50000": [0xdb, 0x1f, 0x00]
}

salary_offset_labels = [
    "-$45,001 and below",
    "-$45,000 to -$34,999",
    "-$35,000 to -$24,999",
    "-$25,000 to -$14,999",
    "-$15,000 to -$4,999",
    "-$5,000 to $4,999",
    "$5,000 to $14,999",
    "$15,000 to $24,999",
    "$25,000 to $34,999",
    "$35,000 to $44,999",
    "$45,000 and above",
]

class SalaryOffsetSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw salary band offset sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Salary Offset Key" in p.keys():
            salary_offset_key = p["Salary Offset Key"]
            colours = salary_offset_colours[salary_offset_key]

        return colours
