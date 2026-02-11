import math

EARTH_RADIUS_MILES = 3958.8


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate great-circle distance between two coordinates in miles.
    """

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    # clamp due to floating point precision
    a = min(1.0, max(0.0, a))

    return 2 * EARTH_RADIUS_MILES * math.asin(math.sqrt(a))
