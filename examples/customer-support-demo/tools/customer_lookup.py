"""Customer lookup tool - simulates CRM database lookup."""

from strands import tool

# Simulated customer database
CUSTOMER_DATABASE = {
    "CUST-12345": {
        "name": "Sarah Johnson",
        "email": "sarah.johnson@example.com",
        "account_status": "active",
        "tier": "Enterprise",
        "customer_since": "2022-03-15",
        "total_spend": 2499.88,
        "previous_tickets": [
            {
                "id": "TKT-9001",
                "date": "2024-06-10",
                "category": "Technical",
                "subject": "Login issues after password reset",
                "resolution": "Cleared browser cache, resolved",
                "satisfaction": 5,
            }
        ],
        "special_notes": "Long-term customer, high value. Prefers email communication.",
        "communication_style": "Professional, detail-oriented",
        "technical_proficiency": "Intermediate",
    },
    "CUST-67890": {
        "name": "TechCorp Inc.",
        "email": "support@techcorp.example.com",
        "account_status": "active",
        "tier": "Enterprise",
        "customer_since": "2021-01-10",
        "total_spend": 24999.00,
        "api_calls_daily": 50000,
        "previous_tickets": [
            {
                "id": "TKT-8500",
                "date": "2024-09-22",
                "category": "Technical",
                "subject": "Rate limiting questions",
                "resolution": "Upgraded plan, increased limits",
                "satisfaction": 4,
            },
            {
                "id": "TKT-8100",
                "date": "2024-07-15",
                "category": "Billing",
                "subject": "Invoice clarification",
                "resolution": "Explained usage-based pricing",
                "satisfaction": 5,
            },
        ],
        "special_notes": "VIP customer. Dedicated account manager: John Smith. SLA: 4-hour response.",
        "communication_style": "Technical, prefers detailed explanations",
        "technical_proficiency": "Expert",
    },
    "CUST-11111": {
        "name": "Analytics Pro LLC",
        "email": "admin@analyticspro.example.com",
        "account_status": "active",
        "tier": "Professional",
        "customer_since": "2022-08-20",
        "total_spend": 4799.76,
        "previous_tickets": [
            {
                "id": "TKT-7200",
                "date": "2024-10-05",
                "category": "Product",
                "subject": "Dashboard customization request",
                "resolution": "Provided workaround using filters",
                "satisfaction": 4,
            }
        ],
        "special_notes": "Heavy Analytics module user. Finance team is primary stakeholder.",
        "communication_style": "Concise, appreciates quick responses",
        "technical_proficiency": "Intermediate",
    },
    "CUST-99999": {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "account_status": "trial",
        "tier": "Trial",
        "customer_since": "2024-12-01",
        "total_spend": 0,
        "previous_tickets": [],
        "special_notes": "New trial user. Evaluating for team of 10.",
        "communication_style": "Casual",
        "technical_proficiency": "Beginner",
    },
}


@tool
def customer_lookup(customer_id: str) -> dict:
    """
    Look up customer information and history from the CRM database.

    Args:
        customer_id: The unique customer identifier (e.g., "CUST-12345")

    Returns:
        A dictionary containing customer information including:
        - name: Customer name
        - email: Contact email
        - account_status: Current account status (active, trial, suspended)
        - tier: Subscription tier (Trial, Professional, Enterprise)
        - customer_since: Account creation date
        - total_spend: Lifetime value
        - previous_tickets: List of past support interactions
        - special_notes: Important account notes
        - communication_style: Preferred communication approach
        - technical_proficiency: Customer's technical level
    """
    if customer_id in CUSTOMER_DATABASE:
        customer = CUSTOMER_DATABASE[customer_id]
        return {
            "status": "found",
            "customer_id": customer_id,
            "data": customer,
            "ticket_count": len(customer.get("previous_tickets", [])),
            "avg_satisfaction": (
                sum(t.get("satisfaction", 0) for t in customer.get("previous_tickets", []))
                / len(customer["previous_tickets"])
                if customer.get("previous_tickets")
                else None
            ),
        }
    else:
        return {
            "status": "not_found",
            "customer_id": customer_id,
            "message": f"No customer found with ID: {customer_id}. Customer may be new or ID may be incorrect.",
            "suggestion": "Proceed with limited context or ask customer for verification.",
        }
