import math
from SunburstOrgWidget import SunburstOrgWidget, fx_rates

salary_offset_colours = {
    "-50%": [0x18, 0x3c, 0xb6],
    "-40%": [0x1e, 0x60, 0xb4],
    "-30%": [0x2d, 0x80, 0xb0],
    "-20%": [0x34, 0x9e, 0x60],
    "-10%": [0x40, 0xaf, 0x13],
    "0%": [0x90, 0xc6, 0x12],
    "10%": [0xfd, 0xfa, 0x19],
    "20%": [0xf8, 0xc7, 0x10],
    "30%": [0xf6, 0x8d, 0x06],
    "40%": [0xf5, 0x61, 0x01],
    "50%": [0xdb, 0x1f, 0x00]
}

class SalaryOffsetSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw salary band offset sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Salary Offset Percentage" in p.keys():
            salary_offset_percentage = p["Salary Offset Percentage"]
            if salary_offset_percentage > 50:
                salary_offset_percentage = 50
            elif salary_offset_percentage < -50:
                salary_offset_percentage = -50

            salary_offset_int = (int(salary_offset_percentage) // 10) * 10
            index = "{}%".format(salary_offset_int)

            colours = salary_offset_colours[index]

        return colours
