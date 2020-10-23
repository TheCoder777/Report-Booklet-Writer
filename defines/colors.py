
"""
Some predefined colors from the colored module
"""

from colored import attr, fg

# Colors for the terminal
RESET = attr("reset")
BOLD = attr(1)
ERROR = fg(1)
WARNING = fg(214)
SUCCESS = fg(2)

# Colors for the HTML templates (defined names in CSS)
MSG_NORMAL = "--text-color"
MSG_WARNING = "--warning-color"
MSG_SUCCESS = "--accent-color"
