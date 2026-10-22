import os
from typing import Any, Dict, List, Optional
from ._models import Day
from ._github_client import fetch_calendar, parse_days
from ._path_finder import dijkstra_shortest_path
from ._svg_builder import build_svg
from ._themes import get_theme


def ensure_directory_exists(file_path: str) -> None:
    directory: str = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)


def write_file(content: str, file_path: str) -> None:
    ensure_directory_exists(file_path)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)


def create_graph(login: str, token: str, output_path: str, theme: str) -> None:
    calendar: Dict[str, Any] = fetch_calendar(login, token)
    days: List[Day] = parse_days(calendar)
    total: int = int(calendar.get("totalContributions", 0))

    svg_content: str = build_svg(days, total,
                                 dijkstra_shortest_path,
                                 get_theme(theme))
    write_file(svg_content, output_path)
    print(f"File {output_path} generated successfully with {len(days)} days.")


def update_contribution_calendar(github_login: str, theme: str = "neon") -> None:
    token: Optional[str] = os.environ.get("CONTRIB_TOKEN")
    if not token:
        raise ValueError("Missing CONTRIB_TOKEN environment variable.")
    output_path: str = "assets/contrib.svg"
    create_graph(github_login, token, output_path, theme)
