import math
import streamlit as st

from data import locations as initial_locations
from data import roads as initial_roads

from graph import create_graph

from gbfs import (
    greedy_best_first_search,
    calculate_route_distance,
    heuristic
)

from visualization import draw_graph


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Smart Delivery Route Finder",
    page_icon=None,
    layout="wide"
)


# ==========================================================
# SESSION STATE
# ==========================================================

if "locations" not in st.session_state:

    st.session_state.locations = initial_locations.copy()


if "roads" not in st.session_state:

    st.session_state.roads = initial_roads.copy()


if "blocked_roads" not in st.session_state:

    st.session_state.blocked_roads = []


# ==========================================================
# TITLE
# ==========================================================

st.title(
    "Smart Delivery Route Finder"
)

st.write(
    "AI-Based Delivery Route Planning System"
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header(
    "Delivery Settings"
)


# ==========================================================
# DYNAMIC LOCATION ADDITION
# ==========================================================

st.sidebar.subheader(
    "Add Delivery Location"
)


new_location_name = st.sidebar.text_input(
    "Location Name"
)


new_x = st.sidebar.number_input(
    "X Coordinate",
    value=1.0,
    step=1.0
)


new_y = st.sidebar.number_input(
    "Y Coordinate",
    value=1.0,
    step=1.0
)


existing_locations = list(
    st.session_state.locations.keys()
)


connect_to = st.sidebar.selectbox(
    "Connect New Location To",
    existing_locations
)


if st.sidebar.button(
    "Add Delivery Location",
    use_container_width=True
):

    name = new_location_name.strip()

    if not name:

        st.sidebar.error(
            "Enter a location name."
        )

    elif name in st.session_state.locations:

        st.sidebar.error(
            "This location already exists."
        )

    else:

        # Add location

        st.session_state.locations[name] = (
            new_x,
            new_y
        )


        # Automatically calculate road distance

        x1, y1 = st.session_state.locations[
            connect_to
        ]

        distance = math.sqrt(
            (new_x - x1) ** 2 +
            (new_y - y1) ** 2
        )


        # Add road

        st.session_state.roads.append(
            (
                connect_to,
                name,
                round(distance, 2)
            )
        )


        st.sidebar.success(
            f"{name} added successfully."
        )

        st.rerun()


# ==========================================================
# LOCATION SELECTION
# ==========================================================

location_names = list(
    st.session_state.locations.keys()
)


start = st.sidebar.selectbox(
    "Starting Location",
    location_names,
    index=location_names.index(
        "Warehouse"
    )
)


destination = st.sidebar.selectbox(
    "Delivery Destination",
    location_names
)


# ==========================================================
# ROAD CONDITIONS
# ==========================================================

st.sidebar.subheader(
    "Road Conditions"
)


condition_options = [
    "Normal",
    "Busy",
    "Heavy",
    "Blocked"
]


road_conditions = {}

blocked_roads = []


for source, target, distance in (
    st.session_state.roads
):

    road_name = (
        f"{source} → {target}"
    )


    condition = st.sidebar.selectbox(
        road_name,
        condition_options,
        key=f"condition_{road_name}"
    )


    road = (
        source,
        target
    )


    if condition == "Blocked":

        blocked_roads.append(
            road
        )

    else:

        road_conditions[road] = (
            condition
        )


# ==========================================================
# FIND ROUTE
# ==========================================================

find_route = st.sidebar.button(
    "Find Delivery Route",
    use_container_width=True
)


# ==========================================================
# CREATE GRAPH
# ==========================================================

graph = create_graph(
    st.session_state.locations,
    st.session_state.roads,
    blocked_roads,
    road_conditions
)


# ==========================================================
# NETWORK
# ==========================================================

st.subheader(
    "Delivery Network"
)


fig = draw_graph(
    graph,
    st.session_state.locations,
    start=start,
    destination=destination
)


st.pyplot(fig)


# ==========================================================
# CURRENT LOCATIONS
# ==========================================================

with st.expander(
    "View Delivery Locations"
):

    for name, position in (
        st.session_state.locations.items()
    ):

        st.write(
            f"**{name}** — "
            f"({position[0]:.1f}, "
            f"{position[1]:.1f})"
        )


# ==========================================================
# ROUTE SEARCH
# ==========================================================

if find_route:

    if start == destination:

        st.warning(
            "Starting location and destination "
            "cannot be the same."
        )

    else:

        route, explored, decision_log = (
            greedy_best_first_search(
                graph,
                st.session_state.locations,
                start,
                destination
            )
        )


        # ==================================================
        # ROUTE FOUND
        # ==================================================

        if route:

            total_distance = (
                calculate_route_distance(
                    graph,
                    route
                )
            )


            st.success(
                "Delivery route found successfully."
            )


            # ==================================================
            # METRICS
            # ==================================================

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Route Distance",
                    f"{total_distance:.2f} km"
                )


            with col2:

                st.metric(
                    "Locations Explored",
                    len(explored)
                )


            with col3:

                st.metric(
                    "Route Stops",
                    len(route)
                )


            # ==================================================
            # ROUTE
            # ==================================================

            st.subheader(
                "Selected Delivery Route"
            )


            st.success(
                " → ".join(route)
            )


            # ==================================================
            # SEARCH PROCESS
            # ==================================================

            st.subheader(
                "Search Process"
            )


            st.write(
                " → ".join(explored)
            )


            # ==================================================
            # HEURISTIC VALUES
            # ==================================================

            st.subheader(
                "Heuristic Evaluation"
            )


            for location in explored:

                h_value = heuristic(
                    st.session_state.locations,
                    location,
                    destination
                )


                st.write(
                    f"{location} → "
                    f"{h_value:.2f}"
                )


            # ==================================================
            # AI DECISION LOG
            # ==================================================

            st.subheader(
                "AI Decision Log"
            )


            for step in decision_log:

                st.write(
                    "• " + step
                )


            # ==================================================
            # ROUTE VISUALIZATION
            # ==================================================

            st.subheader(
                "AI Route Visualization"
            )


            route_fig = draw_graph(
                graph,
                st.session_state.locations,
                route=route,
                explored=explored,
                start=start,
                destination=destination
            )


            st.pyplot(
                route_fig
            )


            # ==================================================
            # BLOCKED ROADS
            # ==================================================

            if blocked_roads:

                st.subheader(
                    "Blocked Roads"
                )


                for road in blocked_roads:

                    st.write(
                        f"{road[0]} → {road[1]}"
                    )


        else:

            st.error(
                "No route could be found with "
                "the current road conditions."
            )


# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.caption(
    "Smart Delivery Route Finder | "
    "Greedy Best-First Search"
)