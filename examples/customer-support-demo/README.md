# Customer Support Demo - Before vs After Agent SOP

This demo project demonstrates the dramatic difference between AI agents operating **without** structured guidance versus agents following a **Standard Operating Procedure (SOP)**.

## The Problem

Without structured workflows, AI customer support agents:
- Jump to generic answers without understanding the issue
- Miss important customer context and history
- Provide inconsistent responses across similar tickets
- Skip documentation and follow-up steps
- Handle escalations poorly

## The Solution

The **Customer Support Ticket Resolution SOP** provides:
- Systematic 6-step workflow (Receive → Context → Investigate → Resolve → Document → Follow-up)
- Clear constraints using RFC 2119 keywords (MUST, SHOULD, MAY)
- Tool integration for customer lookup, ticket categorization, and knowledge base search
- Consistent artifact production for audit and training

## Quick Start

### Prerequisites

- Python 3.10+
- AWS credentials configured (for Amazon Bedrock)
- Model access enabled for Claude in us-west-2

### Installation

```bash
# Navigate to the demo directory
cd examples/customer-support-demo

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install strands-agents strands-agents-tools
```

### Running the Demo

```bash
# Interactive demo - choose scenarios
python demo.py

# Run specific scenario
python demo.py --scenario simple_billing
python demo.py --scenario complex_technical
python demo.py --scenario angry_customer

# Run all scenarios
python demo.py --all

# Compare just one agent type
python demo.py --before-only --scenario simple_billing
python demo.py --after-only --scenario simple_billing
```

## Demo Scenarios

| Scenario | Description | Key Difference |
|----------|-------------|----------------|
| `simple_billing` | Duplicate charge complaint | Before: quick refund. After: root cause + goodwill credit |
| `complex_technical` | API timeout blocking production | Before: generic troubleshooting. After: full diagnostics + escalation |
| `feature_request` | PDF export request | Before: "we'll consider it". After: workaround + roadmap info |
| `frustrated_customer` | Login issues with frustration | Before: ignores emotion. After: empathy + systematic resolution |
| `angry_customer` | Escalation demand after delays | Before: defensive. After: de-escalation + immediate action |
| `time_sensitive` | Dashboard down before meeting | Before: standard response. After: urgent workaround + follow-up |

## Project Structure

```
customer-support-demo/
├── README.md               # This file
├── pyproject.toml          # Python project configuration
├── demo.py                 # Main demo runner
├── data/
│   └── sample_tickets.json # Sample support tickets
├── sops/
│   └── customer-support-ticket.sop.md  # The SOP definition
├── agents/
│   ├── before_agent.py     # Agent WITHOUT SOP (minimal)
│   └── after_agent.py      # Agent WITH SOP (structured)
└── tools/
    ├── customer_lookup.py  # Simulated CRM lookup
    ├── ticket_categorizer.py  # Ticket classification
    └── knowledge_base.py   # KB search
```

## The SOP Workflow

The Customer Support Ticket Resolution SOP enforces this 6-step workflow:

### 1. Receive and Categorize
- Classify ticket type (Billing, Technical, Account, Product, Complaint)
- Assess priority (P1-Critical to P4-Low)
- Determine complexity (Simple, Moderate, Complex)

### 2. Gather Context
- Look up customer history
- Review previous tickets
- Check account status and tier
- Note special accommodations

### 3. Investigate and Diagnose
- Analyze symptoms
- Form and test hypotheses
- Search knowledge base
- Determine root cause

### 4. Resolve or Escalate
- Apply solution if within scope
- Escalate with full context if needed
- Provide workarounds when appropriate

### 5. Document Resolution
- Create comprehensive resolution record
- Update knowledge base if new solution
- Log product feedback

### 6. Follow-up and Close
- Verify customer satisfaction
- Schedule follow-up per SLA
- Close ticket with confirmation

## Before vs After Comparison

### Example: Duplicate Charge Ticket

**BEFORE (No SOP):**
```
"I'm sorry about that. I've refunded one charge. Is there anything else?"
```

**AFTER (With SOP):**
```
Step 1 - Categorization:
  Category: Billing > Duplicate Charge
  Priority: P2-High

Step 2 - Context:
  Customer since 2022, Enterprise tier, no previous billing issues

Step 3 - Diagnosis:
  Root cause: Dec 14 maintenance side effect (47 accounts affected)

Step 4 - Resolution:
  - Refunded $29.99
  - Applied 1-month goodwill credit
  - Flagged for engineering review

Step 5 - Documentation:
  Resolution logged, KB updated, incident linked

Step 6 - Follow-up:
  7-day check-in scheduled, feedback requested

Response:
  "Hi Sarah, Thank you for bringing this to our attention. I've reviewed
   your account and can confirm you were charged twice due to a system
   issue during our December 14th maintenance window..."
```

## Custom Tools

### customer_lookup
Simulates CRM database lookup returning:
- Account status and tier
- Previous tickets and satisfaction scores
- Special notes and communication preferences

### categorize_ticket
Analyzes ticket text to suggest:
- Category and subcategory
- Priority with reasoning
- Complexity assessment
- Sentiment indicators

### search_knowledge_base
Searches internal documentation for:
- Relevant articles
- Solution steps
- Known issues and workarounds

## Sample Data

The `data/sample_tickets.json` contains 8 diverse scenarios based on the [Kaggle Customer Support Ticket Dataset](https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset) format (CC0 license).

To use your own data:
1. Download from Kaggle: `kaggle datasets download -d suraj520/customer-support-ticket-dataset`
2. Convert to the JSON format in `sample_tickets.json`
3. Run the demo with your data

## Video Recording Tips

For the best demo video:

1. **Start with the problem**: Show the "before" agent giving a one-line response
2. **Introduce the SOP**: Briefly show the workflow diagram
3. **Show the transformation**: Run the "after" agent on the same ticket
4. **Highlight artifacts**: Point out each step's output
5. **Emphasize consistency**: Run multiple scenarios to show reliability

Recommended scenarios for video:
- `simple_billing` - Quick, clear before/after
- `angry_customer` - Shows empathy handling
- `complex_technical` - Shows escalation workflow

## Resources

- [Agent SOPs Documentation](https://github.com/strands-agents/agent-sops)
- [Strands Agents SDK](https://strandsagents.com)
- [AWS Blog: Introducing Strands Agent SOPs](https://aws.amazon.com/blogs/opensource/introducing-strands-agent-sops-natural-language-workflows-for-ai-agents/)
