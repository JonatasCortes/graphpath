import os
from typing import Any, Dict, List, Optional
from .models import Day
from .github_client import fetch_calendar, parse_days
from .path_finder import dijkstra_shortest_path
from .svg_builder import build_svg
from .themes import get_theme
import argparse
import sys


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


def update_contribution_calendar(github_login: str, theme: str = "neon", output_path: str = "assets/contrib.svg") -> None:
    token: Optional[str] = os.environ.get("GH_TOKEN")
    if not token:
        raise ValueError("Missing GH_TOKEN environment variable.")
    create_graph(github_login, token, output_path, theme)


def main() -> int:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate the graphpath SVG for a GitHub profile."
    )
    parser.add_argument("username", help="GitHub username")
    parser.add_argument("--theme", default="neon",
                        help="theme name (default: neon)")
    arguments: argparse.Namespace = parser.parse_args()
    username: str = str(arguments.username)
    theme_name: str = str(arguments.theme)
    output_path: str = "assets/contrib.svg"

    try:
        update_contribution_calendar(username, theme_name, output_path)
    except Exception as error:
        print(f"graphpath: {error}", file=sys.stderr)
        return 1
    print(f"graphpath: saved {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
