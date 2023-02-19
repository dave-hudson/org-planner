import math

from SunburstOrgWidget import SunburstOrgWidget

rollup_salary_colours = {
    "$10,000": [0x20, 0xff, 0x20],
    "$31,600": [0x3c, 0xe4, 0x3c],
    "$100,000": [0x58, 0xd8, 0x58],
    "$316,000": [0x74, 0xac, 0x74],
    "$1,000,000": [0x90, 0x90, 0x90],
    "$3,160,000": [0xac, 0x74, 0xac],
    "$10,000,000": [0xc8, 0x58, 0xc8],
    "$31,600,000": [0xe4, 0x3c, 0xe4],
    "$100,000,000": [0xff, 0x20, 0xff]
}

class RollupSalarySunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw rollup salary sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        rollup_salary = p["Rollup Salaries"]
        if rollup_salary > 0:
            log_rollup_salary = math.log10(rollup_salary) - 4
            base_colour = int(0x38 * log_rollup_salary)
            colours = [0x20 + base_colour, 0xff - base_colour, 0x20 + base_colour, 0xff]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p["Name"]

        tt += f"\nRollup Salaries: ${p['Rollup Salaries']:,.0f}"
        rollup_missing_salaries = self._people[uen]["Missing Salaries"]
        if rollup_missing_salaries > 0:
            ppl = "People"
            if rollup_missing_salaries == 1:
                ppl = "Person"

            tt += f" (Missing {rollup_missing_salaries} {ppl})"

        return tt
