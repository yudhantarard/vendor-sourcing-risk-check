"""Google Places API (New) - Text Search returning several candidates."""
import requests

URL = "https://places.googleapis.com/v1/places:searchText"
FIELDS = ",".join(f"places.{f}" for f in (
    "id", "displayName", "primaryType", "types", "rating", "userRatingCount", "formattedAddress",
    "nationalPhoneNumber", "websiteUri", "businessStatus", "googleMapsUri"))


class PlacesError(Exception):
    """User-safe failure message."""


def _call_api(query: str, api_key: str, limit: int) -> dict:
    try:
        r = requests.post(
            URL, timeout=10,
            headers={"X-Goog-Api-Key": api_key, "X-Goog-FieldMask": FIELDS, "Content-Type": "application/json"},
            json={"textQuery": query, "pageSize": limit, "languageCode": "id", "regionCode": "ID"})
    except requests.Timeout:
        raise PlacesError("Google Places timed out.")
    except requests.RequestException:
        raise PlacesError("Google Places could not be reached.")
    if r.status_code in (401, 403):
        raise PlacesError("Google Places rejected the API key (authentication/permission).")
    if r.status_code == 429:
        raise PlacesError("Google Places quota exceeded.")
    if r.status_code != 200:
        raise PlacesError(f"Google Places returned HTTP {r.status_code}.")
    try:
        return r.json()
    except ValueError:
        raise PlacesError("Google Places returned an unexpected response.")


def _norm(p: dict) -> dict:
    return {
        "id": p.get("id") or p.get("googleMapsUri") or str(hash(str(p))),
        "name": (p.get("displayName") or {}).get("text") or "Unnamed business",
        "rating": p.get("rating"), "total_reviews": p.get("userRatingCount"),
        "address": p.get("formattedAddress"), "phone": p.get("nationalPhoneNumber"),
        "website": p.get("websiteUri"), "business_status": p.get("businessStatus"),
        # The Places API has no authoritative claimed/unclaimed field.
        "verification_status": "Not independently verified", "maps_url": p.get("googleMapsUri"),
        "primary_type": p.get("primaryType"), "types": p.get("types") or [], "source": "Google Places API",
    }


def search_google(query: str, location: str | None, api_key: str, limit: int = 10) -> list[dict]:
    """Return vendors from Google Places. Raises PlacesError with a user-safe message."""
    text = f"{query} {location}".strip() if location else query
    try:
        return [_norm(x) for x in _call_api(text, api_key, limit).get("places") or []]
    except PlacesError:
        raise
    except Exception:
        raise PlacesError("Google Places is unavailable.")
