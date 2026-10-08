import networkx as nx


def create_graph(
    locations,
    roads,
    blocked_roads=None,
    road_conditions=None
):

    graph = nx.Graph()

    if blocked_roads is None:
        blocked_roads = []

    if road_conditions is None:
        road_conditions = {}

    # ------------------------------------------------------
    # Add locations
    # ------------------------------------------------------

    for location, position in locations.items():

        graph.add_node(
            location,
            pos=position
        )

    # ------------------------------------------------------
    # Add roads
    # ------------------------------------------------------

    for source, destination, distance in roads:

        road = (source, destination)
        reverse_road = (destination, source)

        # Skip blocked roads

        if (
            road in blocked_roads
            or reverse_road in blocked_roads
        ):
            continue

        # Get road condition

        condition = road_conditions.get(
            road,
            road_conditions.get(
                reverse_road,
                "Normal"
            )
        )

        # Traffic factor

        if condition == "Normal":
            factor = 1.0

        elif condition == "Busy":
            factor = 1.2

        elif condition == "Heavy":
            factor = 1.5

        else:
            factor = 1.0

        effective_distance = distance * factor

        graph.add_edge(
            source,
            destination,
            weight=effective_distance,
            actual_distance=distance,
            condition=condition
        )

    return graph