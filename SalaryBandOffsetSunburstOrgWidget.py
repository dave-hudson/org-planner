from currencies import currencies
from SunburstOrgWidget import SunburstOrgWidget

salary_band_offset_colours = {
    "-5": [0x18, 0x3c, 0xb6],
    "-4": [0x1e, 0x60, 0xb4],
    "-3": [0x2d, 0x80, 0xb0],
    "-2": [0x34, 0x9e, 0x60],
    "-1": [0x40, 0xaf, 0x13],
    "0": [0x90, 0x90, 0x90],
    "1": [0xfd, 0xfa, 0x19],
    "2": [0xf8, 0xc7, 0x10],
    "3": [0xf6, 0x8d, 0x06],
    "4": [0xf5, 0x61, 0x01],
    "5": [0xdb, 0x1f, 0x00]
}

salary_band_offset_labels = [
    "-$40,001 and below",
    "-$40,000 to -$30,001",
    "-$30,000 to -$20,001",
    "-$20,000 to -$10,001",
    "-$10,000 to -$1",
    "Within band",
    "$1 to $10,000",
    "$10,001 to $20,000",
    "$20,001 to $30,000",
    "$30,001 to $40,000",
    "$40,001 and above"
]

class SalaryBandOffsetSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw salary band analysis sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        if p.has_salary_band():
            salary_band_offset_key = str(p.get_salary_band_offset_key())
            colours = salary_band_offset_colours[salary_band_offset_key]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p.get_name()

        if p.has_salary_band():
            location = p.get_location()
            salary_val = p.get_salary()
            _, cur_sym = currencies[location]
            tt += f"\nSalary: {cur_sym}{salary_val:,}"
            salary_usd_val = p.get_salary_usd()
            tt += f" (${salary_usd_val:,.0f})"

            salary_band_lower_limit = p.get_salary_band_lower_limit()
            salary_band_upper_limit = p.get_salary_band_upper_limit()
            salary_band = (
                f"{cur_sym}{salary_band_lower_limit:,.0f} "
                + f"to {cur_sym}{salary_band_upper_limit:,.0f}"
            )
            salary_band_lower_limit_usd = p.get_salary_band_lower_limit_usd()
            salary_band_upper_limit_usd = p.get_salary_band_upper_limit_usd()
            salary_band_usd = (
                f"${salary_band_lower_limit_usd:,.0f} to ${salary_band_upper_limit_usd:,.0f}"
            )
            tt += f"\nSalary Band: {salary_band} ({salary_band_usd})"
            salary_band_offset = p.get_salary_band_offset()
            tt += (
                f"\nSalary Band Offset: {cur_sym}{salary_band_offset:,.0f}"
                .replace("{cur_sym}-", "-{cur_sym}")
            )
            salary_band_offset_usd = p.get_salary_band_offset_usd()
            tt += f" (${salary_band_offset_usd:,.0f})".replace("$-", "-$")

        return tt
