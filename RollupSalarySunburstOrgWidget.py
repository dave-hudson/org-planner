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
        (rollup_salaries, _) = p.get_rollup_salaries(self._people)
        if rollup_salaries > 0:
            log_rollup_salaries = math.log10(rollup_salaries) - 4
            base_colour = int(0x38 * log_rollup_salaries)
            colours = [0x20 + base_colour, 0xff - base_colour, 0x20 + base_colour, 0xff]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p.get_name()

        (rollup_salaries, missing_salaries) = p.get_rollup_salaries(self._people)
        tt += f"\nRollup Salaries: ${rollup_salaries:,.0f}"
        if missing_salaries > 0:
            ppl = "People"
            if missing_salaries == 1:
                ppl = "Person"

            tt += f" (Missing {missing_salaries} {ppl})"

        return tt
