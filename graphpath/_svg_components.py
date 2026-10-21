import math
from typing import Dict, List, Tuple
from ._constants import (
    ANIMATION_DURATION,
    BASE_RADIUS,
    COLOR_EDGE_PULSE,
    COLOR_NODE_BACKGROUND,
    COLOR_NODE_FILL,
    COLOR_NODE_STROKE,
    CURSOR_TRAVEL_SHARE,
    INNER_RADIUS_RATIO,
    MONTHS,
    OPACITY_MULTIPLIER,
    PATH_VISIBILITY_SHARE,
    PULSE_RADIUS_ADDITION,
    RADIUS_MULTIPLIER,
    STROKE_WIDTH_NORMAL,
    STROKE_WIDTH_THICK,
)
from ._models import Day


def month_labels(days: List[Day]) -> List[Tuple[int, str]]:
    first_of_column: Dict[int, Day] = {}
    
    for day in days:
        first_of_column.setdefault(day.column, day)

    labels: List[Tuple[int, str]] = []
    last_month: int = -1
    
    for column in sorted(first_of_column.keys()):
        month: int = first_of_column[column].when.month
        if month != last_month:
            labels.append((column, MONTHS[month - 1]))
            last_month = month

    if len(labels) > 1 and labels[1][0] - labels[0][0] < 3:
        labels.pop(0)
        
    return labels


def node_radius(count: int, max_count: int) -> float:
    if max_count == 0:
        return BASE_RADIUS
    return BASE_RADIUS + RADIUS_MULTIPLIER * math.sqrt(count / max_count)


def node_svg(x: float, y: float, count: int, max_count: int, tooltip: str = "") -> List[str]:
    radius: float = node_radius(count, max_count)
    opacity: float = 0.4 + OPACITY_MULTIPLIER * (count / max_count) if max_count > 0 else 0.4
    title: str = f"<title>{tooltip}</title>" if tooltip else ""
    
    return [
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{COLOR_NODE_BACKGROUND}" '
        f'stroke="{COLOR_NODE_FILL}" stroke-opacity="{opacity:.2f}" stroke-width="{STROKE_WIDTH_NORMAL}">{title}</circle>',
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius * INNER_RADIUS_RATIO:.1f}" '
        f'fill="{COLOR_NODE_FILL}" fill-opacity="{opacity:.2f}"/>',
    ]


def pixel_distance(first: Day, second: Day) -> float:
    return math.sqrt((first.x - second.x) ** 2 + (first.y - second.y) ** 2)


def light_up(start: float, end: float) -> str:
    return (
        f'<animate attributeName="opacity" dur="{ANIMATION_DURATION}s" repeatCount="indefinite" '
        f'values="0;0;1;1;0" keyTimes="0;{start:.4f};{end:.4f};{PATH_VISIBILITY_SHARE};1"/>'
    )


def build_pulse(route: List[Day], max_count: int) -> List[str]:
    if len(route) < 2:
        return []

    lengths: List[float] = [pixel_distance(route[i], route[i+1]) for i in range(len(route) - 1)]
    total_length: float = sum(lengths)

    arrivals: List[float] = [0.0]
    travelled: float = 0.0
    
    for length in lengths:
        travelled += length
        arrivals.append(CURSOR_TRAVEL_SHARE * (travelled / total_length) if total_length > 0 else 0.0)

    parts: List[str] = []
    for index in range(len(route) - 1):
        first: Day = route[index]
        second: Day = route[index + 1]
        parts.append(
            f'<line x1="{first.x:.1f}" y1="{first.y:.1f}" x2="{second.x:.1f}" y2="{second.y:.1f}" '
            f'stroke="{COLOR_EDGE_PULSE}" stroke-width="{STROKE_WIDTH_THICK}" stroke-linecap="round" opacity="0">'
            f'{light_up(arrivals[index], arrivals[index + 1])}</line>'
        )
        
    for index, day in enumerate(route):
        radius: float = node_radius(day.count, max_count) + PULSE_RADIUS_ADDITION
        parts.append(
            f'<circle cx="{day.x:.1f}" cy="{day.y:.1f}" r="{radius:.1f}" fill="{COLOR_NODE_FILL}" '
            f'fill-opacity=".35" stroke="{COLOR_NODE_STROKE}" stroke-width="{STROKE_WIDTH_NORMAL}" opacity="0">'
            f'{light_up(arrivals[index], arrivals[index] + 0.015)}</circle>'
        )

    path_str: str = " ".join(f'{"M" if i == 0 else "L"}{d.x:.1f},{d.y:.1f}' for i, d in enumerate(route))
    
    parts.append(
        f'<circle r="9" fill="url(#pulse)" opacity="0">'
        f'<animateMotion dur="{ANIMATION_DURATION}s" repeatCount="indefinite" path="{path_str}" '
        f'keyPoints="0;1;1" keyTimes="0;{CURSOR_TRAVEL_SHARE};1" calcMode="linear"/>'
        f'<animate attributeName="opacity" dur="{ANIMATION_DURATION}s" repeatCount="indefinite" '
        f'values="0;1;1;0;0" keyTimes="0;0.01;{CURSOR_TRAVEL_SHARE};{CURSOR_TRAVEL_SHARE + 0.06};1"/>'
        f'</circle>'
    )
    
    return parts