# Fuel Route Optimization API

## Overview
This Django API calculates the most cost-effective fuel stops along a driving route in the USA.

It:
- Retrieves the full driving route using OpenRouteService
- Uses a local dataset of fuel prices
- Selects optimal fuel stops based on cheapest nearby station
- Calculates total fuel cost assuming 10 MPG and 500 mile range

## Architecture
- One external routing API call per request
- No runtime geocoding
- Fuel stations preprocessed and cached locally
- Greedy cost optimization algorithm

## Run locally

pip install -r requirements.txt

Create .env:
ORS_API_KEY=your_key_here

python manage.py runserver

## Endpoint

POST /api/route/

{
  "start": [-118.2437, 34.0522],
  "end": [-74.0060, 40.7128]
}

## Notes
Fuel station coordinates were preprocessed once and cached to ensure fast responses and minimal external API usage.
