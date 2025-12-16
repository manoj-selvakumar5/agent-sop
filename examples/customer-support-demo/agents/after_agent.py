"""
After Agent - Customer support WITH SOP guidance.

This agent demonstrates structured workflow execution using the
Customer Support Ticket Resolution SOP. It will:
- Systematically categorize tickets before responding
- Gather customer context and history
- Investigate root causes methodically
- Produce documented artifacts at each step
- Ensure proper follow-up and closure
"""

from pathlib import Path
from strands import Agent

# Import custom tools
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.customer_lookup import customer_lookup
from tools.ticket_categorizer import categorize_ticket
from tools.knowledge_base import search_knowledge_base


def load_sop() -> str:
    """Load the customer support SOP from the sops directory."""
    sop_path = Path(__file__).parent.parent / "sops" / "customer-support-ticket.sop.md"
    if sop_path.exists():
        return sop_path.read_text()
    else:
        raise FileNotFoundError(f"SOP not found at {sop_path}")


def create_after_agent() -> Agent:
    """
    Create a customer support agent with SOP guidance and tools.

    This agent uses the structured Customer Support Ticket Resolution SOP
    and has access to tools for looking up customers, categorizing tickets,
    and searching the knowledge base.
    """
    sop_content = load_sop()

    return Agent(
        system_prompt=sop_content,
        tools=[customer_lookup, categorize_ticket, search_knowledge_base],
    )


def handle_ticket_after(
    ticket_content: str,
    customer_id: str | None = None,
    priority_override: str | None = None,
    interaction_mode: str = "auto",
) -> str:
    """
    Handle a support ticket using the SOP-guided 'after' agent.

    Args:
        ticket_content: The customer's ticket/message
        customer_id: Optional customer ID for context lookup
        priority_override: Optional priority override (P1-P4)
        interaction_mode: "interactive" or "auto" (default: auto for demo)

    Returns:
        The agent's response with full workflow execution
    """
    agent = create_after_agent()

    # Structured prompt following SOP parameter format
    prompt = f"""Please resolve the following customer support ticket using the SOP workflow.

## Parameters

- **ticket_content**: {ticket_content}
- **customer_id**: {customer_id or "Not provided"}
- **priority_override**: {priority_override or "None - assess during categorization"}
- **interaction_mode**: {interaction_mode}

Please execute all steps of the Customer Support Ticket Resolution SOP:
1. Receive and Categorize
2. Gather Context
3. Investigate and Diagnose
4. Resolve or Escalate
5. Document Resolution
6. Follow-up and Close

For each step, show the artifact produced."""

    result = agent(prompt)
    return result.message


if __name__ == "__main__":
    # Example usage
    sample_ticket = """
    I was charged twice for my subscription last month. My card shows $29.99
    on Dec 1 and Dec 15. Can you help?
    """

    print("=== AFTER Agent Response (with SOP) ===\n")
    response = handle_ticket_after(
        ticket_content=sample_ticket,
        customer_id="CUST-12345",
        interaction_mode="auto",
    )
    print(response)
