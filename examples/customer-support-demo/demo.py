#!/usr/bin/env python3
"""
Customer Support Demo - Before vs After SOP Comparison

This script demonstrates the dramatic difference between:
- BEFORE: An AI agent without structured SOP guidance
- AFTER: An AI agent following the Customer Support Ticket Resolution SOP

Usage:
    python demo.py                    # Interactive demo with all scenarios
    python demo.py --scenario billing # Run specific scenario
    python demo.py --before-only      # Only run the 'before' agent
    python demo.py --after-only       # Only run the 'after' agent
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.before_agent import handle_ticket_before
from agents.after_agent import handle_ticket_after


def load_sample_tickets() -> list:
    """Load sample tickets from JSON file."""
    data_path = Path(__file__).parent / "data" / "sample_tickets.json"
    with open(data_path) as f:
        data = json.load(f)
    return data["tickets"]


def print_separator(char: str = "=", length: int = 80):
    """Print a separator line."""
    print(char * length)


def print_header(text: str):
    """Print a formatted header."""
    print_separator()
    print(f"  {text}")
    print_separator()


def run_comparison(ticket: dict, show_before: bool = True, show_after: bool = True):
    """
    Run the before/after comparison for a single ticket.

    Args:
        ticket: The ticket data dictionary
        show_before: Whether to show the 'before' agent response
        show_after: Whether to show the 'after' agent response
    """
    print_header(f"TICKET: {ticket['ticket_subject']}")
    print(f"\nScenario: {ticket['demo_scenario']}")
    print(f"Customer: {ticket['customer_name']}")
    print(f"Type: {ticket['ticket_type']} | Priority: {ticket['ticket_priority']}")
    print(f"\nTicket Content:")
    print(f"  \"{ticket['ticket_description']}\"")
    print()

    if show_before:
        print_separator("-")
        print("  BEFORE (Without SOP)")
        print_separator("-")
        print()

        try:
            before_response = handle_ticket_before(
                ticket_content=ticket["ticket_description"],
                customer_id=ticket.get("customer_id"),
            )
            print(before_response)
        except Exception as e:
            print(f"Error running before agent: {e}")

        print()

    if show_after:
        print_separator("-")
        print("  AFTER (With SOP + Tools)")
        print_separator("-")
        print()

        try:
            after_response = handle_ticket_after(
                ticket_content=ticket["ticket_description"],
                customer_id=ticket.get("customer_id"),
                interaction_mode="auto",
            )
            print(after_response)
        except Exception as e:
            print(f"Error running after agent: {e}")

        print()

    print_separator("=")
    print()


def interactive_menu(tickets: list):
    """Show interactive menu to select demo scenarios."""
    print_header("Customer Support Demo - Before vs After SOP")
    print()
    print("This demo shows the difference between an AI agent without")
    print("structured guidance (BEFORE) and one following the Customer")
    print("Support Ticket Resolution SOP (AFTER).")
    print()

    print("Available scenarios:")
    print()
    for i, ticket in enumerate(tickets, 1):
        print(f"  {i}. [{ticket['demo_scenario']:20}] {ticket['ticket_subject']}")

    print()
    print("  A. Run ALL scenarios")
    print("  Q. Quit")
    print()

    while True:
        choice = input("Select scenario (1-8, A, or Q): ").strip().upper()

        if choice == "Q":
            print("Goodbye!")
            break
        elif choice == "A":
            for ticket in tickets:
                run_comparison(ticket)
                input("Press Enter to continue to next scenario...")
                print()
        elif choice.isdigit() and 1 <= int(choice) <= len(tickets):
            run_comparison(tickets[int(choice) - 1])
            input("Press Enter to continue...")
        else:
            print("Invalid choice. Please try again.")


def main():
    parser = argparse.ArgumentParser(
        description="Customer Support Demo - Before vs After SOP Comparison"
    )
    parser.add_argument(
        "--scenario",
        choices=[
            "simple_billing",
            "complex_technical",
            "feature_request",
            "frustrated_customer",
            "new_prospect",
            "angry_customer",
            "billing_clarification",
            "time_sensitive",
        ],
        help="Run a specific demo scenario",
    )
    parser.add_argument(
        "--before-only",
        action="store_true",
        help="Only run the 'before' agent (no SOP)",
    )
    parser.add_argument(
        "--after-only",
        action="store_true",
        help="Only run the 'after' agent (with SOP)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all scenarios non-interactively",
    )
    parser.add_argument(
        "--ticket-index",
        type=int,
        help="Run specific ticket by index (1-8)",
    )

    args = parser.parse_args()

    # Load tickets
    tickets = load_sample_tickets()

    # Determine which agents to show
    show_before = not args.after_only
    show_after = not args.before_only

    if args.scenario:
        # Run specific scenario
        for ticket in tickets:
            if ticket["demo_scenario"] == args.scenario:
                run_comparison(ticket, show_before, show_after)
                break
        else:
            print(f"Scenario '{args.scenario}' not found.")
            sys.exit(1)

    elif args.ticket_index:
        # Run specific ticket by index
        if 1 <= args.ticket_index <= len(tickets):
            run_comparison(tickets[args.ticket_index - 1], show_before, show_after)
        else:
            print(f"Invalid ticket index. Must be 1-{len(tickets)}.")
            sys.exit(1)

    elif args.all:
        # Run all scenarios
        for ticket in tickets:
            run_comparison(ticket, show_before, show_after)

    else:
        # Interactive mode
        interactive_menu(tickets)


if __name__ == "__main__":
    main()
