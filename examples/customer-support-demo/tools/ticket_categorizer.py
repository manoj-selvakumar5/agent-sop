"""Ticket categorization tool - analyzes ticket content for classification."""

import re
from strands import tool

# Category keywords mapping
CATEGORY_KEYWORDS = {
    "Billing": {
        "keywords": [
            "charge",
            "charged",
            "invoice",
            "payment",
            "refund",
            "subscription",
            "billing",
            "price",
            "cost",
            "fee",
            "credit card",
            "receipt",
            "upgrade",
            "downgrade",
            "cancel",
            "renewal",
        ],
        "subcategories": {
            "Duplicate Charge": ["twice", "double", "duplicate", "charged twice", "multiple charges"],
            "Refund Request": ["refund", "money back", "return"],
            "Subscription Issue": ["subscription", "renewal", "cancel", "upgrade", "downgrade"],
            "Invoice Question": ["invoice", "receipt", "statement"],
            "Payment Failed": ["failed", "declined", "couldn't process", "payment error"],
        },
    },
    "Technical": {
        "keywords": [
            "error",
            "bug",
            "crash",
            "not working",
            "broken",
            "issue",
            "problem",
            "fail",
            "timeout",
            "slow",
            "api",
            "integration",
            "login",
            "password",
            "access",
            "connection",
        ],
        "subcategories": {
            "API Issue": ["api", "endpoint", "integration", "timeout", "connection"],
            "Login/Access": ["login", "password", "access", "authentication", "sign in", "locked out"],
            "Performance": ["slow", "lag", "performance", "speed", "loading"],
            "Bug Report": ["bug", "error", "crash", "broken", "glitch"],
            "Feature Not Working": ["not working", "doesn't work", "stopped working"],
        },
    },
    "Account": {
        "keywords": [
            "account",
            "profile",
            "settings",
            "email",
            "notification",
            "preference",
            "security",
            "two-factor",
            "2fa",
            "delete account",
        ],
        "subcategories": {
            "Account Settings": ["settings", "preference", "notification", "profile"],
            "Security": ["security", "two-factor", "2fa", "suspicious", "hacked"],
            "Account Deletion": ["delete", "close account", "remove account"],
        },
    },
    "Product": {
        "keywords": [
            "feature",
            "how to",
            "can i",
            "is it possible",
            "export",
            "import",
            "report",
            "dashboard",
            "analytics",
        ],
        "subcategories": {
            "Feature Request": ["would be nice", "request", "suggestion", "wish", "want to be able"],
            "How-To Question": ["how to", "how do i", "can i", "is it possible"],
            "Export/Import": ["export", "import", "download", "csv", "pdf"],
        },
    },
    "Complaint": {
        "keywords": [
            "frustrated",
            "angry",
            "unacceptable",
            "terrible",
            "worst",
            "disappointed",
            "upset",
            "ridiculous",
            "complaint",
        ],
        "subcategories": {
            "Service Complaint": ["service", "support", "response time", "wait"],
            "Product Complaint": ["product", "quality", "doesn't meet"],
            "General Dissatisfaction": ["frustrated", "angry", "disappointed"],
        },
    },
}

# Priority indicators
PRIORITY_INDICATORS = {
    "P1": [
        "urgent",
        "critical",
        "emergency",
        "outage",
        "down",
        "production",
        "blocking",
        "security breach",
        "data loss",
        "cannot use",
        "completely broken",
    ],
    "P2": [
        "important",
        "high priority",
        "business impact",
        "major",
        "significant",
        "affecting many",
        "vip",
        "enterprise",
    ],
    "P3": ["when you can", "moderate", "workaround available", "partial"],
    "P4": ["feature request", "suggestion", "minor", "low priority", "nice to have", "enhancement"],
}


@tool
def categorize_ticket(description: str) -> dict:
    """
    Analyze ticket content and suggest categorization, priority, and complexity.

    Args:
        description: The full ticket description text to analyze

    Returns:
        A dictionary containing:
        - suggested_category: Main category (Billing, Technical, Account, Product, Complaint)
        - suggested_subcategory: Specific subcategory
        - suggested_priority: P1-P4 with reasoning
        - complexity: Simple, Moderate, or Complex
        - keywords_found: Keywords that influenced the categorization
        - sentiment_indicators: Words suggesting customer emotion
        - confidence: Confidence level in the categorization (high, medium, low)
    """
    description_lower = description.lower()

    # Find matching category
    category_scores = {}
    keywords_found = []

    for category, config in CATEGORY_KEYWORDS.items():
        score = 0
        matched_keywords = []
        for keyword in config["keywords"]:
            if keyword in description_lower:
                score += 1
                matched_keywords.append(keyword)
        if score > 0:
            category_scores[category] = {"score": score, "keywords": matched_keywords}
            keywords_found.extend(matched_keywords)

    # Determine best category
    if category_scores:
        best_category = max(category_scores.keys(), key=lambda k: category_scores[k]["score"])
    else:
        best_category = "General Inquiry"

    # Find subcategory
    subcategory = "General"
    if best_category in CATEGORY_KEYWORDS:
        for subcat, subcat_keywords in CATEGORY_KEYWORDS[best_category].get(
            "subcategories", {}
        ).items():
            for keyword in subcat_keywords:
                if keyword in description_lower:
                    subcategory = subcat
                    break

    # Determine priority
    priority = "P3"  # Default
    priority_reason = "Standard priority - no urgent indicators found"

    for p_level, indicators in PRIORITY_INDICATORS.items():
        for indicator in indicators:
            if indicator in description_lower:
                priority = p_level
                priority_reason = f"Contains '{indicator}' indicating {p_level} priority"
                break
        if priority != "P3" or p_level == "P4":
            break

    # Determine complexity
    word_count = len(description.split())
    has_technical_terms = any(
        term in description_lower for term in ["api", "integration", "database", "server", "code"]
    )
    mentions_multiple_issues = description_lower.count(".") > 2 or description_lower.count("and") > 2

    if priority == "P1" or (has_technical_terms and mentions_multiple_issues):
        complexity = "Complex"
    elif has_technical_terms or word_count > 100:
        complexity = "Moderate"
    else:
        complexity = "Simple"

    # Detect sentiment
    sentiment_indicators = []
    negative_words = [
        "frustrated",
        "angry",
        "upset",
        "terrible",
        "awful",
        "unacceptable",
        "disappointed",
    ]
    positive_words = ["please", "thanks", "thank you", "appreciate"]

    for word in negative_words:
        if word in description_lower:
            sentiment_indicators.append(f"negative: {word}")
    for word in positive_words:
        if word in description_lower:
            sentiment_indicators.append(f"positive: {word}")

    # Calculate confidence
    if category_scores and category_scores.get(best_category, {}).get("score", 0) >= 3:
        confidence = "high"
    elif category_scores and category_scores.get(best_category, {}).get("score", 0) >= 1:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "suggested_category": best_category,
        "suggested_subcategory": subcategory,
        "suggested_priority": priority,
        "priority_reason": priority_reason,
        "complexity": complexity,
        "keywords_found": list(set(keywords_found)),
        "sentiment_indicators": sentiment_indicators,
        "confidence": confidence,
        "word_count": word_count,
        "recommendation": (
            f"Categorize as {best_category} > {subcategory}, Priority {priority}, "
            f"Complexity: {complexity}"
        ),
    }
