# ==========================================================
# INITIAL LOCATION DATA
# ==========================================================

locations = {
    "Warehouse": (0, 0),
    "Kukatpally": (2, 4),
    "Miyapur": (4, 1),
    "Bachupally": (5, 5),
    "JNTU": (7, 2),
    "Nizampet": (8, 6),
    "Pragathi Nagar": (10, 3)
}


# ==========================================================
# INITIAL ROADS
# ==========================================================

roads = [
    ("Warehouse", "Kukatpally", 4.5),
    ("Warehouse", "Miyapur", 4.2),

    ("Kukatpally", "Bachupally", 3.1),
    ("Kukatpally", "JNTU", 4.8),

    ("Miyapur", "Bachupally", 3.6),
    ("Miyapur", "JNTU", 4.1),

    ("Bachupally", "Nizampet", 3.2),

    ("JNTU", "Nizampet", 4.0),
    ("JNTU", "Pragathi Nagar", 3.5),

    ("Nizampet", "Pragathi Nagar", 2.8)
]