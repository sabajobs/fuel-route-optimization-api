import csv
import json
import time
import os
import requests
from django.core.management.base import BaseCommand
from pathlib import Path

ORS_GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"
REQUEST_DELAY = 1.2  # respects free tier rate limits


class Command(BaseCommand):
    help = "Geocode fuel stations and cache coordinates locally (resumable)"

    def handle(self, *args, **kwargs):
        base_dir = Path(__file__).resolve().parent.parent.parent
        csv_path = base_dir / "data" / "fuel-prices-for-be-assessment.csv"
        output_path = base_dir / "data" / "fuel_stations_with_coords.json"

        api_key = os.getenv("ORS_API_KEY")
        if not api_key:
            self.stderr.write("ERROR: ORS_API_KEY not set in environment")
            return

        # Load existing cache safely
        results = []
        if output_path.exists():
            try:
                with open(output_path, "r", encoding="utf-8") as f:
                    results = json.load(f)
            except Exception:
                self.stdout.write("Corrupted cache detected — starting fresh")
                results = []

        # Deduplicate by name+city+state
        processed = {(r["name"], r["city"], r["state"]) for r in results}

        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for idx, row in enumerate(reader, start=1):
                key = (row["Truckstop Name"], row["City"], row["State"])

                if key in processed:
                    continue

                query = f'{row["Truckstop Name"]}, {row["City"]}, {row["State"]}, USA'

                params = {
                    "api_key": api_key,
                    "text": query,
                    "size": 1
                }

                try:
                    response = requests.get(ORS_GEOCODE_URL, params=params, timeout=20)
                    response.raise_for_status()
                    data = response.json()

                    if not data.get("features"):
                        self.stdout.write(f"Skipped (no result): {query}")
                        continue

                    coords = data["features"][0]["geometry"]["coordinates"]

                    record = {
                        "name": row["Truckstop Name"],
                        "city": row["City"],
                        "state": row["State"],
                        "price": float(row["Retail Price"]),
                        "lat": coords[1],
                        "lng": coords[0],
                    }

                    results.append(record)
                    processed.add(key)

                    # atomic write (prevents corruption)
                    temp_path = output_path.with_suffix(".tmp")
                    with open(temp_path, "w", encoding="utf-8") as out:
                        json.dump(results, out, indent=2)
                    temp_path.replace(output_path)

                    self.stdout.write(f"Saved {len(results)} stations")
                    time.sleep(REQUEST_DELAY)

                except Exception as e:
                    self.stderr.write(f"Failed: {query} | {e}")
                    time.sleep(3)

        self.stdout.write("Geocoding complete.")
