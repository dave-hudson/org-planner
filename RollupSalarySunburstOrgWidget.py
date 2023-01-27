import math
from SunburstOrgWidget import SunburstOrgWidget, fx_rates

rollup_salary_colours = {
    "10000": [0x20, 0xff, 0x20],
    "31600": [0x3c, 0xe4, 0x3c],
    "100000": [0x58, 0xd8, 0x58],
    "316000": [0x74, 0xac, 0x74],
    "1000000": [0x90, 0x90, 0x90],
    "3160000": [0xac, 0x74, 0xac],
    "10000000": [0xc8, 0x58, 0xc8],
    "31600000": [0xe4, 0x3c, 0xe4],
    "100000000": [0xff, 0x20, 0xff]
}

class RollupSalarySunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw rollup salary sunburst org charts.
    """
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        rollup_salary = p["Rollup Salaries"]
        if rollup_salary > 0:
            log_rollup_salary = math.log10(rollup_salary) - 4
            base_colour = int(0x38 * log_rollup_salary)
            colours = [0x20 + base_colour, 0xff - base_colour, 0x20 + base_colour, 0xff]

        return colours
