"""Clearly labelled mock vendors. Never real-world facts."""


def get_mock_vendors(query: str, location: str | None = None) -> list[dict]:
    where = f"{location or 'Jakarta'}, Indonesia (mock address)"
    specs = [("A", "printing_service", 4.6, 212, "OPERATIONAL"),
             ("B", "manufacturer", 4.2, 88, "OPERATIONAL"),
             ("C", "corporate_office", 3.9, 31, "OPERATIONAL"),
             ("D", "wholesaler", 4.4, 154, "CLOSED_TEMPORARILY")]
    return [{
        "id": f"mock-{k}", "name": f"Mock Vendor {k} ({query})", "rating": r, "total_reviews": n,
        "address": where, "phone": "+62 21 XXXXXXXX", "website": "https://example.com",
        "business_status": st, "verification_status": "Mock / Not Verified", "maps_url": None,
        "primary_type": t, "types": [], "source": "Mock Data",
    } for k, t, r, n, st in specs]
