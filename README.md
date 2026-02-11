# Fuel Route Optimization API

## Overview

This project provides a Django REST API that calculates cost-effective
fuel stops along a driving route inside the USA.

Given a start and end coordinate, the API: - Retrieves the driving route
using OpenRouteService - Finds nearby fuel stations from a preprocessed
dataset - Selects cheapest stations along the route - Calculates total
fuel cost

Vehicle assumptions: - Fuel tank range: 500 miles - Fuel efficiency: 10
miles per gallon

------------------------------------------------------------------------

## Architecture

**Key design goals** - Only ONE external routing API call per request -
No runtime geocoding (all stations preprocessed) - Fast deterministic
responses - Simple greedy optimization strategy

**Flow**

1.  Client sends start & end coordinates
2.  Backend fetches route geometry
3.  Local dataset scanned for nearby stations
4.  Cheapest stations selected when fuel is low
5.  Total cost returned

------------------------------------------------------------------------

## Setup (Run Locally)

### 1. Clone & install

    pip install -r requirements.txt

### 2. Create environment file

Create `.env` in project root:

    ORS_API_KEY=your_api_key_here
    DJANGO_SECRET_KEY=dev-secret-key

### 3. Run database migrations

    python manage.py migrate

### 4. Start server

    python manage.py runserver

------------------------------------------------------------------------

## API Usage

### Endpoint

    POST /api/route/

### Request

``` json
{
  "start": [-118.2437, 34.0522],
  "end": [-74.0060, 40.7128]
}
```

### Response

``` json
{
  "summary": {
    "distance_miles": 2794.42,
    "estimated_gallons_used": 279.44,
    "total_fuel_cost": 329.4,
    "number_of_stops": 2
  },
  "fuel_stops": [
    {
      "lat": 39.580339,
      "lng": -104.988082,
      "price_per_gallon": 3.299,
      "gallons_filled": 50.0,
      "cost": 164.95
    }
  ]
}
```

------------------------------------------------------------------------

## Data Processing

The provided fuel dataset did not contain coordinates.

A preprocessing command was implemented:

    python manage.py geocode_stations

This geocodes stations once and stores them locally:

    routing/data/fuel_stations_with_coords.json

At runtime the API only reads this cached file → fast responses and
minimal API usage.

------------------------------------------------------------------------

## Notes

-   Coordinates must be `[longitude, latitude]`
-   Only routes inside the USA are supported
-   Designed for clarity and reliability rather than over-optimization
