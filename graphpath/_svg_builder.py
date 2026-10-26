from typing import List, Tuple
from ._constants import (
    CALENDAR_TITLE,
    EMPTY_NODE_RADIUS,
    FONT_FAMILY,
    ORIGIN_X,
    ORIGIN_Y,
    STEP_SIZE,
    SVG_HEIGHT,
    SVG_WIDTH,
    WEEKDAY_LABELS,
)
from ._graph import build_edges, connect_groups
from ._models import Day
from ._path_finder import Pathfinder
from ._svg_components import build_pulse, month_labels, node_svg


def build_svg(days: List[Day], total: int, pathfinder: Pathfinder, theme: dict[str, str]) -> str:
    max_count: int = max((day.count for day in days), default=0)
    active_days: List[Day] = [day for day in days if day.count > 0]
    parts: List[str] = []

    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
        f'viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}" role="img" aria-labelledby="t d">'
    )
    parts.append('<title id="t">Contribution graph</title>')
    parts.append(
        '<desc id="d">Each node is a day with contributions; node size is the number of contributions.</desc>')

    parts.append('<defs>')
    parts.append('<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">')
    parts.append(
        f'<stop stop-color="{theme["COLOR_BORDER_GRADIENT_START"]}"/><stop offset="1" stop-color="{theme["COLOR_BORDER_GRADIENT_END"]}"/></linearGradient>')
    parts.append('<radialGradient id="glow" cx=".5" cy=".5" r=".5">')
    parts.append(
        f'<stop stop-color="{theme["COLOR_GLOW"]}" stop-opacity=".22"/>')
    parts.append(
        f'<stop offset="1" stop-color="{theme["COLOR_GLOW"]}" stop-opacity="0"/></radialGradient>')
    parts.append('<radialGradient id="pulse">')
    parts.append(
        f'<stop stop-color="{theme["COLOR_PULSE_CORE"]}" stop-opacity=".95"/>')
    parts.append(
        f'<stop offset=".35" stop-color="{theme["COLOR_PULSE_HALO"]}" stop-opacity=".9"/>')
    parts.append(
        f'<stop offset="1" stop-color="{theme["COLOR_PULSE_HALO"]}" stop-opacity="0"/></radialGradient>')
    parts.append('</defs>')

    parts.append(
        f'<rect x="1.5" y="1.5" width="897" height="247" rx="15" fill="{theme["COLOR_BACKGROUND"]}"/>')
    parts.append(
        '<ellipse cx="450" cy="130" rx="420" ry="110" fill="url(#glow)"/>')
    parts.append(
        f'<rect x="22" y="22" width="4" height="22" rx="2" fill="{theme["COLOR_TITLE_BAR"]}"/>')
    parts.append(
        f'<text x="37" y="39" font-family="{FONT_FAMILY}" font-size="18" font-weight="700" fill="{theme["COLOR_TITLE_TEXT"]}">{CALENDAR_TITLE}</text>')

    parts.append(
        f'<text x="878" y="39" text-anchor="end" font-family="{FONT_FAMILY}" font-size="13" fill="{theme["COLOR_SUMMARY_TEXT"]}">')
    parts.append(
        f'<tspan font-size="20" font-weight="700" fill="{theme["COLOR_TOTAL_NUMBER"]}">{total}</tspan> contributions ')
    parts.append(
        f'<tspan font-size="20" font-weight="700" fill="{theme["COLOR_ACTIVE_DAYS_NUMBER"]}">{len(active_days)}</tspan> active days in the last year</text>')

    for column, name in month_labels(days):
        x: float = ORIGIN_X + column * STEP_SIZE - 4
        parts.append(
            f'<text x="{x:.1f}" y="74" font-family="{FONT_FAMILY}" font-size="15" fill="{theme["COLOR_MONTH_LABEL"]}">{name}</text>')

    for row, w_name in WEEKDAY_LABELS.items():
        y: float = ORIGIN_Y + row * STEP_SIZE + 4
        parts.append(
            f'<text x="42" y="{y:.1f}" text-anchor="end" font-family="{FONT_FAMILY}" font-size="15" fill="{theme["COLOR_WEEKDAY_LABEL"]}">{w_name}</text>')

    parts.append(f'<g fill="{theme["COLOR_EMPTY_NODE"]}">')
    for day in days:
        if day.count == 0:
            parts.append(
                f'<circle cx="{day.x:.1f}" cy="{day.y:.1f}" r="{EMPTY_NODE_RADIUS}"/>')
    parts.append('</g>')

    edges: List[Tuple[Day, Day]] = build_edges(active_days)
    edges += connect_groups(active_days, edges)

    parts.append(
        f'<g stroke="{theme["COLOR_EDGE"]}" stroke-width="1" opacity=".42">')
    for first, second in edges:
        parts.append(
            f'<line x1="{first.x:.1f}" y1="{first.y:.1f}" x2="{second.x:.1f}" y2="{second.y:.1f}"/>')
    parts.append('</g>')

    for day in active_days:
        word: str = "contribution" if day.count == 1 else "contributions"
        tooltip: str = f"{day.when.isoformat()}: {day.count} {word}"
        parts.extend(node_svg(day.x, day.y, day.count,
                     max_count, theme, tooltip))

    legend_y: float = 216.0
    middle_count: int = round((1 + max_count) / 2)
    parts.append(
        f'<g font-family="{FONT_FAMILY}" font-size="15" fill="{theme["COLOR_LEGEND_TEXT"]}">')
    parts.append(
        f'<text x="778" y="{legend_y + 4}" text-anchor="end">Less</text>')

    for center_x, count in ((794, 1), (814, middle_count), (834, max_count)):
        parts.extend(node_svg(center_x, legend_y, count, max_count, theme))

    parts.append(f'<text x="850" y="{legend_y + 4}">More</text>')
    parts.append('</g>')

    if len(active_days) >= 2:
        route: List[Day] = pathfinder(
            active_days, edges, active_days[0], active_days[-1])
        parts.extend(build_pulse(route, max_count, theme))

    parts.append(
        f'<rect x="1.5" y="1.5" width="897" height="247" rx="15" fill="none" stroke="url(#edge)" stroke-width="2"/>')
    parts.append('</svg>')

    return "\n".join(parts)
