"""Google News RSS - isolated service."""
from urllib.parse import quote

import feedparser
import requests

from utils.helpers import format_date

RSS = "https://news.google.com/rss/search?q={q}&hl=id&gl=ID&ceid=ID:id"


def fetch_google_news(vendor_name: str, limit: int = 5) -> tuple[list[dict], str | None]:
    """Return (articles, error_message). Never raises."""
    try:
        r = requests.get(RSS.format(q=quote(f'"{vendor_name}"')), timeout=8,
                         headers={"User-Agent": "Mozilla/5.0 VendorRiskCheck/1.0"})
        r.raise_for_status()
        feed = feedparser.parse(r.content)
    except requests.RequestException:
        return [], "Google News could not be reached. Try again later."
    except Exception:
        return [], "Google News returned an unreadable response."
    if feed.bozo and not feed.entries:
        return [], "Google News returned invalid RSS."
    articles = []
    for e in feed.entries:
        try:
            title = (e.get("title") or "").strip()
            link = e.get("link")
            if not title or not link:
                continue
            src = (e.get("source") or {}).get("title")
            if not src and " - " in title:
                title, src = title.rsplit(" - ", 1)
            articles.append({
                "title": title, "source": src or "Unknown source",
                "published": format_date(e.get("published_parsed")), "link": link,
            })
        except Exception:
            continue
        if len(articles) >= limit:
            break
    return articles, None
