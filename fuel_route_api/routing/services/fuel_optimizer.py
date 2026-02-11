from .utils import haversine

MAX_RANGE = 500       # miles per full tank
MPG = 10              # miles per gallon
SEARCH_RADIUS = 25    # miles from route to consider a station
REFUEL_THRESHOLD = 80 # refuel when remaining range drops below this


def stations_near_route_point(point, stations):
    """
    Returns all stations within SEARCH_RADIUS miles of a route point.
    point = [lng, lat]
    """
    lng, lat = point
    nearby = []

    for s in stations:
        if haversine(lat, lng, s["lat"], s["lng"]) <= SEARCH_RADIUS:
            nearby.append(s)

    return nearby


def calculate_fuel_stops(route, stations):
    """
    Greedy strategy:
    - Drive along the route
    - When fuel is low, stop at cheapest nearby station
    - Fill full tank
    """

    geometry = route["geometry"]
    total_distance = route["distance_miles"]

    if not geometry or len(geometry) < 2:
        return [], 0

    stops = []
    total_cost = 0
    fuel_remaining = MAX_RANGE

    # sample route to keep performance fast
    sample_rate = max(1, len(geometry) // 300)

    last_stop_index = -9999  # prevents duplicate nearby stops

    for i in range(sample_rate, len(geometry), sample_rate):

        prev = geometry[i - sample_rate]
        curr = geometry[i]

        # compute actual travelled distance
        step_distance = haversine(prev[1], prev[0], curr[1], curr[0])
        fuel_remaining -= step_distance

        # avoid clustered stops
        if i - last_stop_index < 10:
            continue

        # refuel condition
        if fuel_remaining <= REFUEL_THRESHOLD:

            nearby = stations_near_route_point(curr, stations)
            if not nearby:
                continue

            cheapest = min(nearby, key=lambda s: s["price"])

            gallons = MAX_RANGE / MPG
            cost = gallons * cheapest["price"]

            stops.append({
                "lat": cheapest["lat"],
                "lng": cheapest["lng"],
                "price_per_gallon": round(cheapest["price"], 3),
                "gallons_filled": round(gallons, 2),
                "cost": round(cost, 2),
            })

            total_cost += cost
            fuel_remaining = MAX_RANGE
            last_stop_index = i

    return stops, round(total_cost, 2)
