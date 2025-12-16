"""
Before Agent - Customer support WITHOUT SOP guidance.

This agent demonstrates what happens when an AI handles support tickets
without structured workflow guidance. It will:
- Jump to answers without gathering context
- Miss important customer information
- Provide inconsistent responses
- Skip documentation and follow-up
"""

from strands import Agent


MINIMAL_SYSTEM_PROMPT = """You are a customer support agent. Help customers with their issues.

Be helpful and try to resolve their problems quickly."""


def create_before_agent() -> Agent:
    """
    Create a basic customer support agent without SOP guidance.

    This agent has minimal instructions and no tools, demonstrating
    the "before" state without structured workflows.
    """
    return Agent(
        system_prompt=MINIMAL_SYSTEM_PROMPT,
        # No tools - the agent just responds based on the ticket
    )


def handle_ticket_before(ticket_content: str, customer_id: str | None = None) -> str:
    """
    Handle a support ticket using the unstructured 'before' agent.

    Args:
        ticket_content: The customer's ticket/message
        customer_id: Optional customer ID (ignored by this agent)

    Returns:
        The agent's response
    """
    agent = create_before_agent()

    # Simple prompt - just the ticket content
    prompt = f"Customer ticket:\n\n{ticket_content}"

    if customer_id:
        prompt += f"\n\nCustomer ID: {customer_id}"

    result = agent(prompt)
    return result.message


if __name__ == "__main__":
    # Example usage
    sample_ticket = """
    I was charged twice for my subscription last month. My card shows $29.99
    on Dec 1 and Dec 15. Can you help?
    """

    print("=== BEFORE Agent Response ===\n")
    response = handle_ticket_before(sample_ticket, "CUST-12345")
    print(response)
