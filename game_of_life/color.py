from typing import Optional
#
# Doesn't work yet and might be removed in the future
#
class Color(object):
    def __init__(self, debug=False):
        # Debug parameter
        self.debug = debug

    def hex_to_color(self, hex_color: Optional[str] = None):
        if not hex_color:
            # Debug statement
            if self.debug:
                print('WARNING: Hex could not be converted to color: No hex provided')
            return

        # The color
        color = list()

        for i in range(1, 5, 2):
            color.append(hex_color[])