from SunburstOrgWidget import SunburstOrgWidget

service_duration_colours = {
    "0%": [0xe0, 0xe0, 0xe0],
    "12.5%": [0xe0, 0xc4, 0xc4],
    "25%": [0xe0, 0xa8, 0xa8],
    "37.5%": [0xe0, 0x8c, 0x8c],
    "50%": [0xe0, 0x70, 0x70],
    "62.5%": [0xe0, 0x54, 0x54],
    "75%": [0xe0, 0x38, 0x38],
    "87.5%": [0xe0, 0x1c, 0x1c],
    "100%": [0xe0, 0x00, 0x00]
}

class ServiceDurationSunburstOrgWidget(SunburstOrgWidget):
    """
    A widget class used to draw service duration sunburst org charts.
    """
    def _get_brush_colour(self, uen):
        colours = self._unknown_colour

        p = self._people[uen]
        base_colour = int(0xe0 * p["Service Duration Fraction"])
        colours = [0xe0, 0xe0 - base_colour, 0xe0 - base_colour, 0xff]

        return colours

    def _get_tool_tip(self, uen):
        p = self._people[uen]
        tt = p["Name"]
        tt += f"\nStart Date: {p['Person']['Employments'][-1]['Start Date']}"
        service_duration = p['Service Duration'] / (86400 * 7)
        tt += f"\nService Duration: {service_duration:.1f} weeks"

        return tt
