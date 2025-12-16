"""
Before Agent - Customer support with typical prompt (no SOP).

This agent has the SAME TOOLS as the after_agent, but uses a typical
prompt instead of a structured SOP. This creates a fair comparison
showing the value of SOPs is in structure/workflow, not tooling.
"""

from pathlib import Path
from strands import Agent

# Import custom tools - SAME as after_agent
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.customer_lookup import customer_lookup
from tools.ticket_categorizer import categorize_ticket
from tools.knowledge_base import search_knowledge_base


TYPICAL_PROMPT = """
You are a helpful customer support agent for a SaaS company.

Your job is to help customers with their billing questions and issues.
Be polite, professional, and try to resolve their problems.
If you can help them, do so. If you can't, apologize and offer to escalate.

You have access to these tools:
- customer_lookup: Look up customer history and account info
- categorize_ticket: Help classify the ticket type and priority
- search_knowledge_base: Find relevant solutions and documentation

Remember to:
- Be friendly and empathetic
- Help resolve billing issues
- Offer refunds when appropriate
- Use the tools to gather information
- Thank them for being a customer
"""


def create_before_agent() -> Agent:
    """
    Create a customer support agent with typical prompt (no SOP).

    This agent has the same tools as after_agent but uses a typical
    prompt instead of structured SOP workflow.
    """
    return Agent(
        system_prompt=TYPICAL_PROMPT,
        tools=[customer_lookup, categorize_ticket, search_knowledge_base],  # SAME TOOLS
    )


def handle_ticket_before(ticket_content: str, customer_id: str | None = None) -> str:
    """
    Handle a support ticket using the typical prompt agent.

    Args:
        ticket_content: The customer's ticket/message
        customer_id: Optional customer ID for context lookup

    Returns:
        The agent's response
    """
    agent = create_before_agent()

    prompt = f"Customer ticket:\n\n{ticket_content}"

    if customer_id:
        prompt += f"\n\nCustomer ID: {customer_id}"

    result = agent(prompt)
    return result.message


if __name__ == "__main__":
    sample_ticket = """
    Hey, few things:
    1. I got charged $49.99 but I'm on the $29.99 Basic plan - what happened?
    2. Can I get a receipt for tax purposes?
    3. I'm thinking of canceling - what happens to my data?
    """

    print("=== BEFORE Agent Response (typical prompt) ===\n")
    response = handle_ticket_before(sample_ticket, "CUST-12345")
    print(response)
