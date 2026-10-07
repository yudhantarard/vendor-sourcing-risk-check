"""OpenStreetMap search (free, no key): Nominatim for names, Overpass for categories in a city."""
import re

import requests

from data.sectors import CATEGORY_TAGS

NOMINATIM = "https://nominatim.openstreetmap.org/search"
OVERPASS = "https://overpass-api.de/api/interpreter"
HEADERS = {"User-Agent": "SHIFT-VendorRiskCheck/1.0 (personal procurement screening)"}  # required by Nominatim policy


class OsmError(Exception):
    """User-safe failure message."""


def _get_json(method: str, url: str, **kw):
    try:
        r = requests.request(method, url, headers=HEADERS, timeout=20, **kw)
        r.raise_for_status()
        return r.json()
    except requests.Timeout:
        raise OsmError("OpenStreetMap timed out.")
    except requests.RequestException:
        raise OsmError("OpenStreetMap could not be reached.")
    except ValueError:
        raise OsmError("OpenStreetMap returned an unexpected response.")


def _link(osm_type: str, osm_id) -> str:
    return f"https://www.openstreetmap.org/{osm_type}/{osm_id}"


def _vendor(osm_type, osm_id, name, address, tags: dict, ptype) -> dict:
    return {
        "id": f"osm-{osm_type}-{osm_id}", "name": name, "rating": None, "total_reviews": None,
        "address": address, "phone": tags.get("phone") or tags.get("contact:phone"),
        "website": tags.get("website") or tags.get("contact:website"), "business_status": None,
        "verification_status": "Community-edited map data, not verified",
        "maps_url": _link(osm_type, osm_id), "primary_type": ptype, "types": [], "source": "OpenStreetMap",
    }


def _address(tags: dict) -> str | None:
    parts = [tags.get("addr:street"), tags.get("addr:housenumber"), tags.get("addr:suburb"),
             tags.get("addr:city"), tags.get("addr:postcode")]
    return tags.get("addr:full") or (", ".join(p for p in parts if p) or None)


def _tag_of(tags: dict, wanted: list[str]) -> str | None:
    return next((w for w in wanted if tags.get(w.split("=")[0]) == w.split("=")[1]), None)


def _nominatim(params: dict) -> list[dict]:
    return _get_json("GET", NOMINATIM, params={"format": "jsonv2", "addressdetails": 1, "extratags": 1,
                                                "namedetails": 1, "countrycodes": "id", **params})


def _by_text(query: str, location: str | None, limit: int) -> list[dict]:
    out = []
    for p in _nominatim({"q": f"{query} {location or ''}".strip(), "limit": limit}):
        tags = p.get("extratags") or {}
        name = (p.get("namedetails") or {}).get("name") or p.get("name")
        if not name:
            continue
        out.append(_vendor(p.get("osm_type"), p.get("osm_id"), name, p.get("display_name"), tags,
                           f"{p.get('category')}={p.get('type')}"))
    return out


def _category_tags(query: str) -> list[str]:
    q = query.lower().strip()
    if re.match(r"^(pt|cv|ud|pd|koperasi)\b", q) or " tbk" in q:  # a company name, not a category
        return []
    return next((tags for words, tags in CATEGORY_TAGS.items() if any(w in q for w in words)), [])


def _by_category(tags: list[str], location: str, limit: int) -> list[dict]:
    geo = _nominatim({"q": location, "limit": 1})
    if not geo:
        return []
    s, n, w, e = geo[0]["boundingbox"]
    body = "".join(f'nwr["{t.split("=")[0]}"="{t.split("=")[1]}"]["name"]({s},{w},{n},{e});' for t in tags)
    data = _get_json("POST", OVERPASS, data={"data": f"[out:json][timeout:20];({body});out center tags {limit};"})
    out = []
    for el in data.get("elements", []):
        t = el.get("tags") or {}
        out.append(_vendor(el["type"], el["id"], t["name"], _address(t), t, _tag_of(t, tags)))
    return out


def search_osm(query: str, location: str | None = None, limit: int = 10) -> list[dict]:
    """Category + city -> Overpass; otherwise (or if empty) Nominatim text search. Raises OsmError."""
    tags = _category_tags(query)
    if tags and location:
        found = _by_category(tags, location, limit)
        if found:
            return found
    return _by_text(query, location, limit)
