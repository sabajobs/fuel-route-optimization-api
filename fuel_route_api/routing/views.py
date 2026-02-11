from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services.routing import get_route
from .services.pricing_loader import load_fuel_prices
from .services.fuel_optimizer import calculate_fuel_stops

MPG = 10


def valid_coords(coords):
    """
    Validate coordinate format: [longitude, latitude]
    """
    if not isinstance(coords, list) or len(coords) != 2:
        return False

    try:
        lon = float(coords[0])
        lat = float(coords[1])
    except (TypeError, ValueError):
        return False

    # basic geographic bounds check
    return -180 <= lon <= 180 and -90 <= lat <= 90


class RouteAPIView(APIView):
    """
    POST /api/route/
    Calculates optimal fuel stops between two coordinates.
    """

    def post(self, request):

        start = request.data.get("start")
        end = request.data.get("end")

        if not valid_coords(start) or not valid_coords(end):
            return Response(
                {"error": "Coordinates must be [longitude, latitude] within valid range"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 1: Get route
        try:
            route = get_route(start, end)
        except Exception as e:
            return Response(
                {"error": "Routing service failed", "details": str(e)},
                status=status.HTTP_502_BAD_GATEWAY
            )

        # Step 2: Calculate fuel stops
        try:
            stations = load_fuel_prices()
            stops, total_cost = calculate_fuel_stops(route, stations)
        except Exception as e:
            return Response(
                {"error": "Fuel calculation failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        gallons_used = route["distance_miles"] / MPG

        return Response({
            "summary": {
                "distance_miles": route["distance_miles"],
                "estimated_gallons_used": round(gallons_used, 2),
                "total_fuel_cost": total_cost,
                "number_of_stops": len(stops),
            },
            "fuel_stops": stops
        })
