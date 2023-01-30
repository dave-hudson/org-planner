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
    def __init__(self) -> None:
        super().__init__()

    def _get_brush_colour(self, uen):
        colours = [0x40, 0x40, 0x40]

        p = self._people[uen]
        if "Salary Band Offset USD Key" in p.keys():
            salary_band_offset_usd_key = p["Salary Band Offset USD Key"]
            colours = salary_band_offset_colours[str(salary_band_offset_usd_key)]

        return colours
