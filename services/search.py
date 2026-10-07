"""Vendor search dispatcher: Google Places if a key is set, else free OpenStreetMap; mock if all fail."""
from data.mock_vendor import get_mock_vendors
from services.osm import OsmError, search_osm
from services.places import PlacesError, search_google


def find_vendors(query: str, location: str | None = None,
                 google_key: str | None = None) -> tuple[list[dict], str | None]:
    """Return (vendors, warning). Never raises."""
    warn = None
    if google_key:
        try:
            found = search_google(query, location, google_key)
            if found:
                return found, None
            warn = "No Google Maps listings found. Showing OpenStreetMap results."
        except PlacesError as e:
            warn = f"{e} Showing OpenStreetMap results instead."
    try:
        found = search_osm(query, location)
        if found:
            return found, warn
        return [], (warn or "") + " No map listings found. Try other words, or add the vendor manually."
    except OsmError as e:
        return get_mock_vendors(query, location), f"{e} Showing fallback (mock) data."
    except Exception:
        return get_mock_vendors(query, location), "Map search is unavailable. Showing fallback (mock) data."
