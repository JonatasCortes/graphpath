from typing import Dict, List

CALENDAR_TITLE: str = "CONTRIBUTION CALENDAR"
MONTHS: List[str] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
WEEKDAY_LABELS: Dict[int, str] = {1: "Mon", 3: "Wed", 5: "Fri"}
FONT_FAMILY: str = "Arial,Helvetica,sans-serif"

ANIMATION_DURATION: float = 12.0
CURSOR_TRAVEL_SHARE: float = 0.72
PATH_VISIBILITY_SHARE: float = 0.92

COLOR_BACKGROUND: str = "#0d0d0d"
COLOR_LABEL: str = "#ff9999"
COLOR_HIGHLIGHT: str = "#ff9999"
COLOR_SOFT_TEXT: str = "#ff9999"
COLOR_LEGEND: str = "#ff9999"
COLOR_NODE_BACKGROUND: str = "#141016"
COLOR_NODE_FILL: str = "#ff4257"
COLOR_NODE_STROKE: str = "#ff8a98"
COLOR_EDGE: str = "#b82a46"
COLOR_EDGE_PULSE: str = "#ff5a6e"
COLOR_EMPTY_NODE: str = "#2a2326"
COLOR_GRADIENT_START: str = "#ff3659"
COLOR_GRADIENT_END: str = "#7b142b"
COLOR_GLOW: str = "#a81d3d"
COLOR_WHITE: str = "#ffffff"

MAX_NEIGHBORS: int = 3
MAX_DISTANCE: float = 3.0
BASE_RADIUS: float = 3.2
RADIUS_MULTIPLIER: float = 3.0
INNER_RADIUS_RATIO: float = 0.45
BASE_OPACITY: float = 0.4
OPACITY_MULTIPLIER: float = 0.6
STROKE_WIDTH_NORMAL: float = 1.6
STROKE_WIDTH_THIN: float = 1.0
STROKE_WIDTH_THICK: float = 2.0
EMPTY_NODE_RADIUS: float = 1.1
PULSE_RADIUS_ADDITION: float = 1.8

SVG_WIDTH: int = 900
SVG_HEIGHT: int = 250
ORIGIN_X: float = 57.8
ORIGIN_Y: float = 91.8
STEP_SIZE: float = 15.55

API_URL: str = "https://api.github.com/graphql"
API_TIMEOUT: int = 30
USER_AGENT: str = "contribution-graph-script"

GRAPHQL_QUERY: str = """
query($login: String!) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}
"""