"""
After Agent - Customer support WITH SOP guidance.

This agent has the SAME TOOLS as before_agent, but uses a structured SOP
instead of a typical prompt. This creates a fair comparison showing
the value of SOPs is in structure/workflow, not tooling.
"""

from pathlib import Path
from strands import Agent

# Import custom tools - SAME as before_agent
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.customer_lookup import customer_lookup
from tools.ticket_categorizer import categorize_ticket
from tools.knowledge_base import search_knowledge_base


def load_sop() -> str:
    """Load the customer support SOP from the sops directory."""
    sop_path = Path(__file__).parent.parent / "sops" / "customer-support.sop.md"
    if sop_path.exists():
        return sop_path.read_text()
    else:
        raise FileNotFoundError(f"SOP not found at {sop_path}")


def create_after_agent() -> Agent:
    """
    Create a customer support agent with SOP guidance.

    This agent has the same tools as before_agent but uses a structured
    SOP workflow instead of typical prompt.
    """
    sop_content = load_sop()

    return Agent(
        system_prompt=sop_content,
        tools=[customer_lookup, categorize_ticket, search_knowledge_base],  # SAME TOOLS
    )


def handle_ticket_after(ticket_content: str, customer_id: str | None = None) -> str:
    """
    Handle a support ticket using the SOP-guided agent.

    Args:
        ticket_content: The customer's ticket/message
        customer_id: Optional customer ID for context lookup

    Returns:
        The agent's response with structured workflow output
    """
    agent = create_after_agent()

    prompt = f"Customer ticket:\n\n{ticket_content}"

    if customer_id:
        prompt += f"\n\nCustomer ID: {customer_id}"

    result = agent(prompt)
    return result.message


if __name__ == "__main__":
    import json

    # Load sample ticket from JSON (multi_issue scenario)
    data_path = Path(__file__).parent.parent / "data" / "sample_tickets.json"
    with open(data_path) as f:
        data = json.load(f)

    # Find the multi_issue scenario ticket
    ticket = next(t for t in data["tickets"] if t["demo_scenario"] == "multi_issue")

    print("=== AFTER Agent Response (with SOP) ===\n")
    response = handle_ticket_after(ticket["ticket_description"], ticket.get("customer_id"))
    print(response)
