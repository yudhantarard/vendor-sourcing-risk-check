"""Risk screening for one or many shortlisted vendors."""
from concurrent.futures import ThreadPoolExecutor

from services.news import fetch_google_news
from services.risk import assess_media_risk


def risk_for(name: str) -> dict:
    """Extend here with registry / sanctions / litigation modules."""
    articles, news_error = fetch_google_news(name, limit=5)
    return {"articles": articles, "news_error": news_error, "risk": assess_media_risk(articles)}


def risk_for_many(names: list[str]) -> dict[str, dict]:
    with ThreadPoolExecutor(max_workers=4) as ex:
        return dict(zip(names, ex.map(risk_for, names)))
