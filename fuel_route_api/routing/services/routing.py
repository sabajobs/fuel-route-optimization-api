import os
import requests

ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"
REQUEST_TIMEOUT = 30


def get_route(start_coords, end_coords):
    """
    Fetch route geometry from OpenRouteService.

    Only one external API call is performed per request.
    Returns distance (miles), duration (hours), and route geometry.
    """

    api_key = os.getenv("ORS_API_KEY")
    if not api_key:
        raise RuntimeError("ORS_API_KEY not configured")

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json",
    }

    body = {
        "coordinates": [start_coords, end_coords]
    }

    response = requests.post(ORS_URL, headers=headers, json=body, timeout=REQUEST_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.HTTPError:
        raise RuntimeError(f"Routing provider error: {response.text}")

    data = response.json()

    if "features" not in data or not data["features"]:
        raise RuntimeError("No route found between provided coordinates")

    feature = data["features"][0]
    segment = feature["properties"]["segments"][0]

    distance_meters = segment["distance"]
    duration_seconds = segment["duration"]
    geometry = feature["geometry"]["coordinates"]  # [lng, lat]

    return {
        "distance_miles": round(distance_meters / 1609.34, 2),
        "duration_hours": round(duration_seconds / 3600, 2),
        "geometry": geometry,
    }
