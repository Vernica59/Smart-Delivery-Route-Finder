import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(
    graph,
    locations,
    route=None,
    explored=None,
    start=None,
    destination=None
):

    fig, ax = plt.subplots(
        figsize=(12, 7)
    )

    pos = locations

    # ------------------------------------------------------
    # Roads
    # ------------------------------------------------------

    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        edge_color="gray",
        width=2
    )

    # ------------------------------------------------------
    # All locations
    # ------------------------------------------------------

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        node_color="lightblue",
        node_size=1800
    )

    # ------------------------------------------------------
    # Explored locations
    # ------------------------------------------------------

    if explored:

        explored_nodes = [
            node
            for node in explored
            if node != start
            and node != destination
        ]

        if explored_nodes:

            nx.draw_networkx_nodes(
                graph,
                pos,
                nodelist=explored_nodes,
                ax=ax,
                node_color="orange",
                node_size=1900
            )

    # ------------------------------------------------------
    # Selected route
    # ------------------------------------------------------

    if route and len(route) > 1:

        route_edges = list(
            zip(
                route[:-1],
                route[1:]
            )
        )

        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=route_edges,
            ax=ax,
            edge_color="red",
            width=4
        )

    # ------------------------------------------------------
    # Start location
    # ------------------------------------------------------

    if start:

        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=[start],
            ax=ax,
            node_color="green",
            node_size=2300
        )

    # ------------------------------------------------------
    # Destination
    # ------------------------------------------------------

    if destination:

        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=[destination],
            ax=ax,
            node_color="red",
            node_size=2300
        )

    # ------------------------------------------------------
    # Labels
    # ------------------------------------------------------

    nx.draw_networkx_labels(
        graph,
        pos,
        ax=ax,
        font_size=9,
        font_weight="bold"
    )

    # ------------------------------------------------------
    # Road distances
    # ------------------------------------------------------

    edge_labels = nx.get_edge_attributes(
        graph,
        "weight"
    )

    edge_labels = {
        edge: f"{distance:.1f} km"
        for edge, distance in edge_labels.items()
    }

    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=edge_labels,
        ax=ax,
        font_size=8
    )

    ax.set_title(
        "Delivery Network"
    )

    ax.axis("off")

    return fig