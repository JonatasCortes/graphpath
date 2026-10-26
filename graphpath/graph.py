from .constants import MAX_DISTANCE, MAX_NEIGHBORS
from typing import Dict, List, Tuple
from datetime import date
from .models import Day
import math


def distance_between(first: Day, second: Day) -> float:
    return math.sqrt((first.column - second.column) ** 2 + (first.row - second.row) ** 2)


def build_edges(active_days: List[Day]) -> List[Tuple[Day, Day]]:
    edges: Dict[Tuple[date, date], Tuple[Day, Day]] = {}

    for day in active_days:
        others: List[Day] = [
            other for other in active_days if other is not day]
        others.sort(key=lambda other: (
            distance_between(day, other), other.when))

        for other in others[:MAX_NEIGHBORS]:
            if distance_between(day, other) > MAX_DISTANCE:
                continue

            sorted_dates: List[date] = sorted([day.when, other.when])
            key: Tuple[date, date] = (sorted_dates[0], sorted_dates[1])
            edges[key] = (day, other)

    return list(edges.values())


def find_group(position: int, parent: List[int]) -> int:
    while parent[position] != position:
        parent[position] = parent[parent[position]]
        position = parent[position]
    return position


def connect_groups(active_days: List[Day], edges: List[Tuple[Day, Day]]) -> List[Tuple[Day, Day]]:
    index_of: Dict[date, int] = {
        day.when: position for position, day in enumerate(active_days)}
    parent: List[int] = list(range(len(active_days)))

    for first, second in edges:
        parent[find_group(index_of[first.when], parent)] = find_group(
            index_of[second.when], parent)

    candidates: List[Tuple[float, Day, Day]] = []
    for position, first in enumerate(active_days):
        for second in active_days[position + 1:]:
            candidates.append((distance_between(first, second), first, second))

    candidates.sort(key=lambda candidate: candidate[0])

    bridges: List[Tuple[Day, Day]] = []
    for _, first, second in candidates:
        group_first: int = find_group(index_of[first.when], parent)
        group_second: int = find_group(index_of[second.when], parent)

        if group_first != group_second:
            parent[group_first] = group_second
            bridges.append((first, second))

    return bridges
