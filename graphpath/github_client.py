
from .constants import API_TIMEOUT, API_URL, GRAPHQL_QUERY, USER_AGENT
from datetime import date
from .models import Day
from typing import Any
import urllib.request
import json


def fetch_calendar(login: str, token: str) -> dict[str, Any]:
    payload: bytes = json.dumps({
        "query": GRAPHQL_QUERY,
        "variables": {"login": login}
    }).encode("utf-8")

    request: urllib.request.Request = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=API_TIMEOUT) as response:
        body: dict[str, Any] = json.load(response)

    if "errors" in body:
        raise RuntimeError(body["errors"])

    return body["data"]["user"]["contributionsCollection"]["contributionCalendar"]


def parse_days(calendar: dict[str, Any]) -> list[Day]:
    days: list[Day] = []

    for column, week in enumerate(calendar["weeks"]):
        for item in week["contributionDays"]:
            day: Day = Day(
                when=date.fromisoformat(item["date"]),
                count=item["contributionCount"],
                column=column,
                row=item["weekday"],
            )
            days.append(day)

    return days
