import json
from pathlib import Path

_CACHE = None


def load_fuel_prices():
    """
    Load preprocessed fuel station dataset.

    The dataset is loaded once and cached in memory to:
    - avoid repeated disk I/O
    - keep API responses fast
    """

    global _CACHE

    if _CACHE is not None:
        return _CACHE

    path = Path(__file__).resolve().parent.parent / "data" / "fuel_stations_with_coords.json"

    if not path.exists():
        raise FileNotFoundError(
            "Fuel dataset not found. Run: python manage.py geocode_stations"
        )

    with open(path, "r", encoding="utf-8") as f:
        _CACHE = json.load(f)

    return _CACHE
