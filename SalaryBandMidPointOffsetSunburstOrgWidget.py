from SunburstOrgWidget import SunburstOrgWidget

salary_band_mid_point_offset_colours = {
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

salary_band_mid_point_offset_labels = [
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

class SalaryBandMidPointOffsetSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw salary band offset sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if p.has_salary_band():
            salary_band_mid_point_offset_key = str(p.get_salary_band_mid_point_offset_key())
            colours = salary_band_mid_point_offset_colours[salary_band_mid_point_offset_key]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p.get_name()
        if p.has_salary_band():
            tt += (
                f"\nSalary: {p.get_salary_str()} ({p.get_salary_usd_str()})"
                f"\nSalary Band Mid Point: {p.get_salary_band_mid_point_str()} "
                f"({p.get_salary_band_mid_point_usd_str()})"
                f"\nSalary Band Mid Point Offset: {p.get_salary_band_mid_point_offset_str()} "
                f"({p.get_salary_band_mid_point_offset_usd_str()})"
            )

        return tt
