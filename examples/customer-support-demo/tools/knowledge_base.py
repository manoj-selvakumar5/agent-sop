"""Knowledge base search tool - simulates internal documentation lookup."""

from strands import tool

# Simulated knowledge base articles
KNOWLEDGE_BASE = [
    {
        "id": "KB-001",
        "title": "How to Reset Your Password",
        "category": "Account",
        "tags": ["password", "login", "access", "reset"],
        "content": """
To reset your password:
1. Go to the login page and click "Forgot Password"
2. Enter your email address
3. Check your inbox for a reset link (check spam folder if not found)
4. Click the link and create a new password
5. Password must be at least 8 characters with one number and one special character

If you don't receive the email within 5 minutes, contact support.
        """,
        "solution_steps": [
            "Direct user to login page",
            "Have them click 'Forgot Password'",
            "Verify email is correct in system",
            "Check for email delivery issues if not received",
        ],
    },
    {
        "id": "KB-002",
        "title": "Understanding Your Invoice",
        "category": "Billing",
        "tags": ["invoice", "billing", "charges", "subscription"],
        "content": """
Your invoice includes:
- Subscription base fee (billed monthly/annually)
- Usage-based charges (API calls, storage, etc.)
- Any add-ons or premium features
- Applicable taxes

Billing cycle runs from the 1st to the last day of each month.
Invoices are generated on the 1st and payment is due within 15 days.
        """,
        "solution_steps": [
            "Explain invoice line items",
            "Clarify billing cycle",
            "Direct to billing portal for detailed breakdown",
        ],
    },
    {
        "id": "KB-003",
        "title": "Duplicate Charge Resolution",
        "category": "Billing",
        "tags": ["duplicate", "charge", "refund", "billing error"],
        "content": """
If a customer reports duplicate charges:
1. Verify the charges in the billing system
2. Check for known billing issues (see incident log)
3. If duplicate confirmed, process refund immediately
4. Apply goodwill credit if appropriate (typically 1 month for Enterprise customers)
5. Document the incident for engineering review

Common causes:
- System maintenance side effects
- Payment gateway timeouts causing retry
- Customer accidentally clicking pay multiple times
        """,
        "solution_steps": [
            "Verify duplicate in billing system",
            "Process refund for duplicate amount",
            "Consider goodwill credit",
            "Flag for engineering if systemic",
        ],
    },
    {
        "id": "KB-004",
        "title": "API Timeout Troubleshooting",
        "category": "Technical",
        "tags": ["api", "timeout", "integration", "connection", "error"],
        "content": """
For API timeout errors:
1. Check current API status at status.example.com
2. Verify customer's timeout settings (default 30s may need increase)
3. Review rate limiting - customer may be hitting limits
4. Check for regional latency issues
5. Recommend implementing retry logic with exponential backoff

Temporary workarounds:
- Increase timeout to 60s
- Implement retry logic (max 3 retries)
- Use regional endpoints if available

If issue persists after troubleshooting, escalate to Infrastructure team.
        """,
        "solution_steps": [
            "Check system status page",
            "Verify timeout configuration",
            "Review rate limit usage",
            "Recommend retry logic implementation",
            "Escalate to Infrastructure if unresolved",
        ],
    },
    {
        "id": "KB-005",
        "title": "Export Formats Available",
        "category": "Product",
        "tags": ["export", "csv", "pdf", "report", "download"],
        "content": """
Currently supported export formats:
- CSV: Full data export, all reports
- JSON: API response format
- Excel: Available for Pro and Enterprise plans

PDF export is on the roadmap for Q2 2025.

Workaround for PDF needs:
1. Export to CSV
2. Open in Excel or Google Sheets
3. Format as needed
4. Print to PDF

For automated PDF generation, consider third-party integrations.
        """,
        "solution_steps": [
            "Explain available formats",
            "Provide PDF workaround",
            "Mention roadmap timeline if customer requests PDF",
            "Suggest third-party integration options",
        ],
    },
    {
        "id": "KB-006",
        "title": "Handling Angry Customers",
        "category": "Process",
        "tags": ["angry", "frustrated", "complaint", "escalation", "de-escalation"],
        "content": """
When dealing with frustrated customers:
1. Acknowledge their feelings: "I understand this is frustrating..."
2. Apologize for the inconvenience (even if not our fault)
3. Focus on solution, not explanation
4. Avoid defensive language
5. Offer concrete next steps and timeline
6. If requested, escalate to supervisor/manager

Key phrases:
- "I completely understand your frustration"
- "Let me make this right for you"
- "Here's exactly what I'm going to do..."
- "I'll personally follow up to ensure this is resolved"
        """,
        "solution_steps": [
            "Acknowledge and empathize",
            "Apologize sincerely",
            "Focus on solution",
            "Provide clear next steps",
            "Escalate if requested",
        ],
    },
    {
        "id": "KB-007",
        "title": "December 2024 Maintenance - Known Issues",
        "category": "Incident",
        "tags": ["maintenance", "december", "billing", "duplicate", "outage"],
        "content": """
INCIDENT: December 14, 2024 Maintenance Window

Known issues from this maintenance:
1. Duplicate billing charges for some customers (47 accounts affected)
   - Cause: Payment processor retry during maintenance
   - Resolution: Auto-refund processed for most, manual review for edge cases

2. Temporary API latency increase (US-East region)
   - Cause: Database migration
   - Resolution: Resolved within 2 hours

If customer reports issues from Dec 14-15, check against this incident first.
        """,
        "solution_steps": [
            "Verify customer was affected by Dec 14 incident",
            "Process refund if duplicate charge confirmed",
            "Apply goodwill credit as appropriate",
            "Reference incident ID: INC-2024-1214",
        ],
    },
]


@tool
def search_knowledge_base(query: str) -> dict:
    """
    Search the internal knowledge base for relevant articles and solutions.

    Args:
        query: Search query describing the issue or topic

    Returns:
        A dictionary containing:
        - results: List of matching articles with relevance scores
        - total_matches: Number of articles found
        - top_recommendation: The most relevant article
        - suggested_solutions: Combined solution steps from top matches
    """
    query_lower = query.lower()
    query_words = set(query_lower.split())

    results = []

    for article in KNOWLEDGE_BASE:
        score = 0
        matched_tags = []
        matched_in_title = False
        matched_in_content = False

        # Check tags
        for tag in article["tags"]:
            if tag in query_lower:
                score += 3
                matched_tags.append(tag)

        # Check title
        title_lower = article["title"].lower()
        for word in query_words:
            if word in title_lower and len(word) > 3:
                score += 2
                matched_in_title = True

        # Check content
        content_lower = article["content"].lower()
        for word in query_words:
            if word in content_lower and len(word) > 3:
                score += 1
                matched_in_content = True

        if score > 0:
            results.append(
                {
                    "article_id": article["id"],
                    "title": article["title"],
                    "category": article["category"],
                    "relevance_score": score,
                    "matched_tags": matched_tags,
                    "matched_in_title": matched_in_title,
                    "matched_in_content": matched_in_content,
                    "content_preview": article["content"][:200].strip() + "...",
                    "solution_steps": article["solution_steps"],
                }
            )

    # Sort by relevance
    results.sort(key=lambda x: x["relevance_score"], reverse=True)

    # Get top recommendation
    top_recommendation = results[0] if results else None

    # Combine solution steps from top 3 matches
    suggested_solutions = []
    for result in results[:3]:
        for step in result.get("solution_steps", []):
            if step not in suggested_solutions:
                suggested_solutions.append(step)

    return {
        "query": query,
        "total_matches": len(results),
        "results": results[:5],  # Return top 5
        "top_recommendation": top_recommendation,
        "suggested_solutions": suggested_solutions[:10],  # Top 10 unique steps
        "message": (
            f"Found {len(results)} relevant article(s)"
            if results
            else "No matching articles found. Consider escalating or creating new KB article."
        ),
    }
