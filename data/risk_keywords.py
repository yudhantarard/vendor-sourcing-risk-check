"""Configurable adverse-media keywords (English + Bahasa Indonesia)."""

HIGH_RISK = [
    "corruption", "korupsi", "fraud", "penipuan", "bribery", "suap",
    "money laundering", "pencucian uang", "sanctions", "sanksi",
    "criminal", "pidana", "terrorism", "terorisme",
]
MEDIUM_RISK = [
    "investigation", "investigasi", "lawsuit", "gugatan", "default", "pailit",
    "bankruptcy", "bangkrut", "illegal", "scam", "tersangka", "dituntut",
]
KEYWORDS = {"HIGH": HIGH_RISK, "MEDIUM": MEDIUM_RISK}
