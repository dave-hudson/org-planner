from currencies import currencies, fx_rates
from SunburstOrgWidget import SunburstOrgWidget

salary_mid_band_offset_colours = {
    "-5": [0x18, 0x3c, 0xb6],
    "-4": [0x1e, 0x60, 0xb4],
    "-3": [0x2d, 0x80, 0xb0],
    "-2": [0x34, 0x9e, 0x60],
    "-1": [0x40, 0xaf, 0x13],
    "0": [0x90, 0xc6, 0x12],
    "1": [0xfd, 0xfa, 0x19],
    "2": [0xf8, 0xc7, 0x10],
    "3": [0xf6, 0x8d, 0x06],
    "4": [0xf5, 0x61, 0x01],
    "5": [0xdb, 0x1f, 0x00]
}

salary_mid_band_offset_labels = [
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

class SalaryMidBandOffsetSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw salary band offset sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if "Salary Offset Key" in p.keys():
            salary_mid_band_offset_key = p["Salary Offset Key"]
            colours = salary_mid_band_offset_colours[salary_mid_band_offset_key]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
<<<<<<< HEAD:SalaryMidBandOffsetSunburstOrgWidget.py
        tt = p["Person"]["Name"]
        if "Salaries" in p["Person"].keys():
            location = p["Person"]["Locations"][-1]["Location"]
            salary_val = p["Person"]["Salaries"][-1]["Salary"]
            _, cur_sym = currencies[location]
            tt += f"\nSalary: {cur_sym}{salary_val:,}"
            salary_usd_val = salary_val * fx_rates[location]
            tt += f" (${salary_usd_val:,.0f})"

=======
        tt = p["Name"]
>>>>>>> e3216db (Simplify people data management.):SalaryOffsetSunburstOrgWidget.py
        if "Salary Offset" in p.keys():
            location = p["Locations"][-1]["Location"]
            _, cur_sym = currencies[location]
            salary_band_mid_point = f"{cur_sym}{p['Salary Band Mid Point']:,.0f}"
            salary_band_mid_point_usd = f"${p['Salary Band Mid Point USD']:,.0f}"
            tt += f"\nSalary Mid-band: {salary_band_mid_point} ({salary_band_mid_point_usd})"
            tt += (
                f"\nSalary Mid-band Offset: {cur_sym}{p['Salary Offset']:,.0f}"
                .replace(f"{cur_sym}-", f"-{cur_sym}")
            )
            tt += f" (${p['Salary Offset USD']:,.0f})".replace("$-", "-$")

        return tt
