"""Transparent keyword-based Preliminary Risk Indicator.

Replaceable: any function with the signature assess_media_risk(articles) -> dict
(e.g. NLP / LLM / entity-matching) can be swapped in via screening.py.
"""
import re

from data.risk_keywords import KEYWORDS

ACTIONS = {
    "LOW": "Continue standard supplier due diligence.",
    "MEDIUM": "Perform manual media review and validate the underlying event. "
              "Consider enhanced supplier due diligence.",
    "HIGH": "Escalate to Compliance / Legal / Procurement leadership for enhanced "
            "due diligence before supplier approval or award.",
}


def _hits(text: str, words: list[str]) -> list[str]:
    return [w for w in words if re.search(rf"\b{re.escape(w)}\b", text, re.I)]


def assess_media_risk(articles: list[dict]) -> dict:
    flagged, levels = [], set()
    for a in articles:
        for level, words in KEYWORDS.items():
            found = _hits(a["title"], words)
            if found:
                levels.add(level)
                flagged.append({"level": level, "keywords": found, "article": a})
    level = "HIGH" if "HIGH" in levels else "MEDIUM" if "MEDIUM" in levels else "LOW"
    findings = [f"{len(articles)} recent article(s) screened (headlines only)."]
    if flagged:
        for f in flagged:
            findings.append(f"{f['level']} keyword(s) {', '.join(f['keywords'])} in: "
                            f"\"{f['article']['title']}\" ({f['article']['source']})")
        findings.append("Each flagged article requires manual context review.")
        if level == "HIGH":
            findings.append("Supplier should undergo enhanced due diligence.")
    else:
        findings.append("No configured adverse keywords detected.")
    findings.append("Company identity should still be validated.")
    return {"level": level, "findings": findings, "flagged": flagged,
            "action": ACTIONS[level], "method": "Keyword matching on headlines"}
