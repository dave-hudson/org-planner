import math
from SunburstOrgWidget import SunburstOrgWidget, fx_rates

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
        if "Salaries" in p["Person"].keys():
            salary = p["Person"]["Salaries"][-1]["Salary"]
            salary_usd = salary * fx_rates[p["Person"]["Locations"][-1]["Location"]]
            log_salary_usd = 0
            if salary >= 10000:
                log_salary_usd = math.log10(salary_usd) - 4

            base_colour = int(0x70 * log_salary_usd)
            colours = [0x20 + base_colour, 0x20 + base_colour, 0xff - base_colour, 0xff]

        return colours
