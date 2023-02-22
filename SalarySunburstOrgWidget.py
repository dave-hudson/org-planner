import math

from SunburstOrgWidget import SunburstOrgWidget

salary_colours = {
    "$10,000": [0x20, 0x20, 0xff],
    "$17,783": [0x3c, 0x3c, 0xe4],
    "$31,600": [0x58, 0x58, 0xd8],
    "$56,234": [0x74, 0x74, 0xac],
    "$100,000": [0x90, 0x90, 0x90],
    "$177,830": [0xac, 0xac, 0x74],
    "$316,000": [0xc8, 0xc8, 0x58],
    "$562,340": [0xe4, 0xe4, 0x3c],
    "$1,000,000": [0xff, 0xff, 0x20]
}

class SalarySunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw salary sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if p.has_salary():
            salary_usd = p.get_salary_usd()
            log_salary_usd = 0
            if salary_usd >= 10000:
                log_salary_usd = math.log10(salary_usd) - 4

            base_colour = int(0x70 * log_salary_usd)
            colours = [0x20 + base_colour, 0x20 + base_colour, 0xff - base_colour, 0xff]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p.get_name()
        if p.has_salary():
            tt += f"\nSalary: {p.get_salary_str()} ({p.get_salary_usd_str()})"

        return tt
