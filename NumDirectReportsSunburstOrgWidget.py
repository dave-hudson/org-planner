from SunburstOrgWidget import SunburstOrgWidget

num_direct_reports_colours = {
    "0": [0x90, 0x90, 0x90],
    "1": [0x18, 0x3c, 0xb6],
    "2": [0x1e, 0x60, 0xb4],
    "3": [0x2d, 0x80, 0xb0],
    "4": [0x34, 0x9e, 0x60],
    "5": [0x40, 0xaf, 0x13],
    "6": [0x90, 0xc6, 0x12],
    "7": [0xfd, 0xfa, 0x19],
    "8": [0xf8, 0xc7, 0x10],
    "9": [0xf6, 0x8d, 0x06],
    "10": [0xf5, 0x61, 0x01],
    "11": [0xdb, 0x1f, 0x00],
    "12": [0xcb, 0x23, 0x3c],
    "13": [0xbb, 0x23, 0x7c],
    "14": [0xa9, 0x2c, 0xb6],
    "15": [0x8c, 0x23, 0xae],
    "16": [0x5c, 0x21, 0xa1],
    "17": [0x5c, 0x21, 0xa1],
    "18": [0x5c, 0x21, 0xa1],
    "19": [0x5c, 0x21, 0xa1],
    "20": [0x5c, 0x21, 0xa1],
}

class NumDirectReportsSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw team sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        num_direct_reports = str(p["Num Direct Reports"])
        if num_direct_reports in num_direct_reports_colours:
            colours = num_direct_reports_colours[num_direct_reports]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p["Name"]
        num_direct_reports = p["Num Direct Reports"]
        if num_direct_reports > 0:
            tt += f"\nDirect Reports: {num_direct_reports}"

        return tt
