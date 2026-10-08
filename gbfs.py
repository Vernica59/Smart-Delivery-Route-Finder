import math
import heapq


# ==========================================================
# HEURISTIC FUNCTION
# ==========================================================

def heuristic(locations, current, goal):

    x1, y1 = locations[current]
    x2, y2 = locations[goal]

    return math.sqrt(
        (x1 - x2) ** 2 +
        (y1 - y2) ** 2
    )


# ==========================================================
# GREEDY BEST-FIRST SEARCH
# ==========================================================

def greedy_best_first_search(
    graph,
    locations,
    start,
    goal
):

    priority_queue = []

    start_h = heuristic(
        locations,
        start,
        goal
    )

    heapq.heappush(
        priority_queue,
        (start_h, start)
    )

    visited = set()

    parent = {
        start: None
    }

    explored_order = []

    decision_log = []

    while priority_queue:

        current_h, current = heapq.heappop(
            priority_queue
        )

        # Already explored
        if current in visited:
            continue

        visited.add(current)

        explored_order.append(current)

        decision_log.append(
            f"Exploring {current} "
            f"(h = {current_h:.2f})"
        )

        # Destination reached
        if current == goal:

            path = []

            node = goal

            while node is not None:

                path.append(node)

                node = parent[node]

            path.reverse()

            decision_log.append(
                f"Destination {goal} reached."
            )

            return (
                path,
                explored_order,
                decision_log
            )

        # Examine neighbors
        neighbors = []

        for neighbor in graph.neighbors(current):

            if neighbor in visited:
                continue

            if neighbor not in parent:

                parent[neighbor] = current

            h = heuristic(
                locations,
                neighbor,
                goal
            )

            neighbors.append(
                (h, neighbor)
            )

        # Lowest heuristic first
        neighbors.sort()

        for h, neighbor in neighbors:

            heapq.heappush(
                priority_queue,
                (h, neighbor)
            )

    decision_log.append(
        "No route could be found."
    )

    return (
        [],
        explored_order,
        decision_log
    )


# ==========================================================
# CALCULATE ROUTE DISTANCE
# ==========================================================

def calculate_route_distance(
    graph,
    route
):

    total_distance = 0

    for i in range(len(route) - 1):

        source = route[i]
        destination = route[i + 1]

        total_distance += (
            graph[source][destination]["weight"]
        )

    return total_distance