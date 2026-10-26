import os
from typing import Any, Dict, List, Optional
from graphpath.models import Day
from graphpath.github_client import fetch_calendar, parse_days
from graphpath.path_finder import dijkstra_shortest_path
from graphpath.svg_builder import build_svg
from graphpath.themes import get_theme, THEMES
from graphpath.main import write_file
import argparse
import sys


def update_assets() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate all assets for the repository."
    )
    parser.add_argument("username", help="GitHub username")
    arguments: argparse.Namespace = parser.parse_args()
    username: str = str(arguments.username)
    output_path: str = "assets/contrib_{theme}.svg"

    try:
        token: Optional[str] = os.environ.get("GH_TOKEN")
        if not token:
            raise ValueError("Missing GH_TOKEN environment variable.")
        calendar: Dict[str, Any] = fetch_calendar(username, token)
        days: List[Day] = parse_days(calendar)
        total: int = int(calendar.get("totalContributions", 0))
        for theme in THEMES:
            svg_content: str = build_svg(days, total,
                                         dijkstra_shortest_path,
                                         get_theme(theme))
            write_file(svg_content, output_path.format(theme=theme))
    except Exception as error:
        print(f"graphpath: {error}", file=sys.stderr)
        return 1
    print(f"graphpath: saved {output_path}")
    return 0


if __name__ == "__main__":
    update_assets()
