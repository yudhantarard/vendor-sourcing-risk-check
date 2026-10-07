"""Sector from map data only (own short list, no AI). Editable in data/sectors.py."""
from data.sectors import OSM_MAP, TYPE_MAP, UNCLEAR


def sector_of(vendor: dict) -> tuple[str, str]:
    """Return (sector, source). Generic types fall through to 'Other / unclear'."""
    src = vendor.get("source")
    if src == "OpenStreetMap" and vendor.get("primary_type") in OSM_MAP:
        return OSM_MAP[vendor["primary_type"]], "OpenStreetMap tag"
    if src in ("Google Places API", "Mock Data"):
        for t in [vendor.get("primary_type"), *(vendor.get("types") or [])]:
            if t in TYPE_MAP:
                return TYPE_MAP[t], "Google Maps type"
    return UNCLEAR, "Not determined"
