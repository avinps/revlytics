from typing import Dict

ASPECT_KEYWORDS = {
    "shipping":  ["shipping", "delivery", "arrived", "dispatch",
                  "late", "fast", "slow", "package", "courier"],
    "quality":   ["quality", "material", "build", "durable",
                  "cheap", "sturdy", "broke", "lasting", "solid"],
    "price":     ["price", "expensive", "cheap", "worth",
                  "value", "cost", "affordable", "overpriced"],
    "support":   ["support", "service", "staff", "helpful",
                  "rude", "responsive", "customer care", "refund"],
    "packaging": ["packaging", "box", "wrapped", "damaged",
                  "pack", "unboxing", "sealed"],
    "usability": ["easy", "difficult", "intuitive", "confusing",
                  "simple", "instructions", "use", "setup"],
}

def extract_aspects(text: str) -> Dict[str, str]:
    text_lower = text.lower()
    found = {}

    for aspect, keywords in ASPECT_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                found[aspect] = keyword
                break

    return found

def aspects_to_string(aspects: Dict[str, str]) -> str:
    if not aspects:
        return ""
    return ",".join(aspects.keys())