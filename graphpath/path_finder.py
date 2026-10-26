from typing import Callable, Dict, List, Tuple
from .graph import distance_between
from datetime import date
from .models import Day
import heapq


Pathfinder = Callable[[List[Day], List[Tuple[Day, Day]], Day, Day], List[Day]]


def dijkstra_shortest_path(active_days: List[Day], edges: List[Tuple[Day, Day]], start: Day, goal: Day,) -> List[Day]:

    by_date: Dict[date, Day] = {day.when: day for day in active_days}
    neighbors_of: Dict[date, List[Day]] = {day.when: [] for day in active_days}

    for first, second in edges:
        neighbors_of[first.when].append(second)
        neighbors_of[second.when].append(first)

    best_cost: Dict[date, float] = {start.when: 0.0}
    came_from: Dict[date, Day] = {}
    queue: List[Tuple[float, date]] = [(0.0, start.when)]

    while queue:
        cost, when = heapq.heappop(queue)

        if when == goal.when:
            break

        if cost > best_cost.get(when, float("inf")):
            continue

        current: Day = by_date[when]

        for neighbor in neighbors_of[when]:
            new_cost: float = cost + distance_between(current, neighbor)

            if new_cost < best_cost.get(neighbor.when, float("inf")):
                best_cost[neighbor.when] = new_cost
                came_from[neighbor.when] = current
                heapq.heappush(queue, (new_cost, neighbor.when))

    if goal.when not in best_cost:
        return []

    route: List[Day] = [goal]
    while route[-1].when != start.when:
        route.append(came_from[route[-1].when])

    route.reverse()
    return route
