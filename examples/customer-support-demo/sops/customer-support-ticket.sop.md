# Customer Support Ticket Resolution

## Overview

This SOP guides AI agents through systematic customer support ticket resolution following a structured Receive, Gather Context, Investigate, Resolve, Document, and Follow-up workflow. It ensures consistent, high-quality customer interactions by enforcing context gathering before response generation, clear escalation criteria, and proper documentation. The agent acts as a Customer Support Specialist - providing empathetic, accurate, and solution-focused assistance while maintaining comprehensive records of all interactions.

## Parameters

- **ticket_content** (required): The full text of the customer support ticket including any subject line, description, and attachments information. This can be provided as direct text, a file path to the ticket, or a structured JSON object with ticket fields
- **customer_id** (optional): Unique identifier for the customer to enable history lookup and context gathering. If not provided, the agent will attempt to extract from ticket content or proceed without historical context
- **priority_override** (optional): Manual priority level (P1-Critical, P2-High, P3-Medium, P4-Low) if pre-determined by triage system. If not provided, priority will be assessed during categorization
- **interaction_mode** (optional, default: "interactive"): The interaction mode:
  - "interactive": Collaboration with user confirmation at key decision points
  - "auto": Autonomous resolution with minimal user interaction after initial setup
- **escalation_contact** (optional): Designated contact or team for escalations. If not provided, will use standard escalation paths
- **sla_hours** (optional, default: 24): Service level agreement response time in hours for follow-up scheduling

**Constraints for parameter acquisition:**
- You MUST ask for all parameters upfront in a single prompt, not just required ones because this ensures efficient workflow and prevents repeated interruptions during execution
- You MUST support multiple input methods for ticket_content (direct input, file path, JSON object)
- You MUST validate that ticket_content contains sufficient information to proceed (minimum: issue description)
- You MUST normalize priority_override input to P1/P2/P3/P4 format if provided in alternative formats
- You MUST confirm successful acquisition of all parameters before proceeding
- If customer_id is not provided, you MUST warn that resolution may be limited without customer history
- If mode is "auto", you MUST warn the user that critical escalation decisions will still require confirmation

## Mode Behavior

Apply these patterns throughout all steps based on the selected mode:

**Interactive Mode:**
- Present ticket categorization and assessment for confirmation before proceeding
- Ask for approval before sending any response to the customer
- Discuss escalation decisions and get confirmation before escalating
- Present resolution options and ask for user preference
- Pause at key decision points to explain reasoning
- Request feedback on response tone and content
- Allow user to modify suggested responses before sending

**Auto Mode:**
- Execute categorization and investigation autonomously
- Document all decisions, assessments, and reasoning in ticket notes
- When multiple resolution approaches exist, select the most appropriate and document why
- Draft responses autonomously but still require human approval for escalations to external teams
- Provide comprehensive summaries at completion
- Escalate automatically only within pre-defined criteria; flag edge cases for review

## Important Notes

**Customer-First Principle:**
This SOP maintains strict focus on customer satisfaction while ensuring accuracy. All responses should be empathetic, clear, and solution-oriented. When in doubt, err on the side of the customer within reasonable policy bounds.

**Artifact Production:**
Each step produces specific artifacts that document the resolution process. These artifacts serve as both audit trail and training data for continuous improvement.

## Steps

### 1. Receive and Categorize

Receive the support ticket and perform initial categorization to determine type, priority, and required expertise.

**Constraints:**
- You MUST create a categorization artifact with the following structure:
  - Ticket ID (generated if not provided)
  - Receipt timestamp
  - Category (Billing, Technical, Account, Product, General Inquiry, Complaint, Feature Request)
  - Subcategory (specific to main category)
  - Assessed Priority (P1-P4) with justification
  - Required expertise/skills
  - Initial complexity assessment (Simple, Moderate, Complex)
- You MUST NOT attempt any resolution before completing categorization because jumping to solutions without understanding the issue leads to incorrect responses
- You MUST identify keywords and phrases indicating urgency or escalation need
- You MUST flag tickets containing sensitive information (personal data, security concerns, legal threats)
- You SHOULD extract the customer's name for personalized responses
- You SHOULD identify the product or service area involved
- You MAY suggest category corrections if the ticket appears miscategorized

**Priority Assessment Criteria:**
- P1-Critical: Service outage, security breach, data loss, complete inability to use product
- P2-High: Major functionality broken, significant business impact, VIP customer
- P3-Medium: Partial functionality issues, workarounds available, general questions
- P4-Low: Feature requests, minor issues, enhancement suggestions

**Artifact Produced:** `categorization_summary`

> See [Mode Behavior](#mode-behavior) for mode-specific interaction guidance

### 2. Gather Context

Collect all relevant information about the customer and their history with the product/service.

**Constraints:**
- You MUST check customer history before drafting any response because context prevents repeated troubleshooting and shows the customer they are valued
- You MUST gather the following context (when available):
  - Customer account status (active, trial, suspended, VIP)
  - Recent interactions and open tickets
  - Purchase history and subscription tier
  - Previous issues with similar products/features
  - Known account preferences or accommodations
- You MUST document when context is unavailable and note impact on resolution approach
- You MUST identify any recurring patterns in customer tickets
- You SHOULD note the customer's communication style from previous interactions
- You SHOULD identify the customer's technical proficiency level
- You MAY flag accounts with unusual patterns for fraud review

**Context Gathering Checklist:**
- [ ] Account status verified
- [ ] Recent ticket history reviewed (last 90 days)
- [ ] Previous related issues identified
- [ ] Customer tier/segment noted
- [ ] Special accommodations or notes reviewed

**Artifact Produced:** `customer_context`

> See [Mode Behavior](#mode-behavior) for mode-specific interaction guidance

### 3. Investigate and Diagnose

Analyze the issue to determine root cause and identify potential solutions.

**Constraints:**
- You MUST investigate systematically before proposing solutions because thorough diagnosis prevents back-and-forth and resolves issues faster
- You MUST document the investigation process including:
  - Symptoms identified from ticket
  - Hypotheses considered
  - Evidence gathered
  - Root cause determination
  - Confidence level in diagnosis
- You MUST consult knowledge base or documentation for similar issues
- You MUST identify if this is a known issue with existing solutions
- You MUST NOT assume the customer's diagnosis is correct because customers often describe symptoms, not root causes
- You SHOULD check for system-wide issues or outages affecting the product
- You SHOULD identify if the issue requires technical access or permissions
- You MAY request additional information from the customer if diagnosis is unclear

**Investigation Framework:**
1. Reproduce or understand the reported behavior
2. Identify what should happen vs. what is happening
3. Determine when the issue started
4. Check for recent changes (customer-side or system-side)
5. Isolate the component causing the issue

**Artifact Produced:** `diagnosis_report`

> See [Mode Behavior](#mode-behavior) for mode-specific interaction guidance

### 4. Resolve or Escalate

Either implement the solution directly or escalate to appropriate team based on complexity and required access.

**Constraints:**
- You MUST follow the resolution path appropriate to the diagnosis
- You MUST NOT escalate without documenting attempted solutions because this wastes specialist time and frustrates customers
- You MUST include in any escalation:
  - Complete context summary (not just ticket forward)
  - Diagnosis and attempted solutions
  - Specific reason for escalation
  - Recommended next steps
  - Customer impact and urgency
- You MUST use the customer's name in responses when available
- You SHOULD draft a response in the customer's communication style
- You SHOULD offer workarounds when permanent solutions require escalation
- You MAY offer proactive suggestions for related issues because this demonstrates expertise and prevents future tickets

**Escalation Criteria:**
- Issue requires system access not available at current tier
- Bug confirmed requiring engineering fix
- Policy exception needed beyond support authority
- Customer explicitly requests escalation after resolution attempt
- Security or compliance concern identified
- Issue unresolved after 3 troubleshooting attempts

**Response Guidelines:**
- Acknowledge the issue and any inconvenience
- Explain what was found and what action was taken
- Set clear expectations for next steps and timeline
- Provide workaround if resolution is not immediate
- Thank the customer for their patience

**Artifact Produced:** `resolution_action`

> See [Mode Behavior](#mode-behavior) for mode-specific interaction guidance

### 5. Document Resolution

Create comprehensive documentation of the resolution for audit, training, and future reference.

**Constraints:**
- You MUST create a resolution record containing:
  - Final status (Resolved, Escalated, Pending Customer, Closed)
  - Resolution summary (2-3 sentences)
  - Root cause category
  - Solution applied
  - Time to resolution
  - Customer satisfaction indicator (if available)
  - Tags for future searchability
- You MUST document any policy exceptions or special accommodations
- You MUST log any product feedback or feature requests extracted from the ticket
- You MUST update knowledge base if a new solution was discovered
- You SHOULD flag systemic issues for product team review
- You SHOULD document any improvement opportunities for process or documentation
- You MAY suggest ticket templates for similar future issues

**Artifact Produced:** `resolution_record`

> See [Mode Behavior](#mode-behavior) for mode-specific interaction guidance

### 6. Follow-up and Close

Ensure customer satisfaction, complete any pending actions, and formally close the ticket.

**Constraints:**
- You MUST schedule follow-up within SLA timeframe for escalated or complex tickets
- You MUST verify resolution with customer before closing (for interactive mode)
- You MUST NOT close tickets without resolution confirmation for P1 and P2 issues because premature closure leads to repeat tickets and customer frustration
- You MUST send closing communication including:
  - Summary of resolution
  - Any relevant documentation or links
  - Invitation for feedback
  - Contact information for further assistance
- You SHOULD request customer satisfaction rating
- You SHOULD offer proactive assistance for related features or issues
- You MAY suggest relevant knowledge base articles or training resources

**Follow-up Schedule:**
- P1/P2: Follow-up within 24 hours of resolution
- P3: Follow-up within 48 hours if customer requested
- P4: Close after resolution, no mandatory follow-up

**Closure Checklist:**
- [ ] Customer confirmed resolution
- [ ] All documentation complete
- [ ] Follow-up scheduled if required
- [ ] Feedback requested
- [ ] Ticket status updated to Closed

**Artifact Produced:** `closure_confirmation`

> See [Mode Behavior](#mode-behavior) for mode-specific interaction guidance

## Desired Outcome

* A fully resolved customer ticket with verified customer satisfaction
* Comprehensive documentation enabling:
  * Audit trail for compliance
  * Training data for agent improvement
  * Knowledge base enhancement
* Consistent customer experience regardless of agent or channel
* Appropriate escalation when required with full context
* Follow-up completed within SLA requirements
* Product feedback captured for continuous improvement

## Examples

### Example 1: Simple Billing Inquiry (Before vs After Comparison)

**BEFORE SOP (Anti-Pattern):**
```
Customer: "I was charged twice for my subscription last month"
Agent: "I'm sorry about that. I've refunded one charge. Is there anything else?"
```
*Problems: No context gathered, no root cause investigation, no documentation, no follow-up*

**AFTER SOP (Correct Pattern):**

**Input:**
```json
{
  "ticket_content": "I noticed I was charged twice for my subscription last month. My card shows $29.99 on Dec 1 and Dec 15. Can you help?",
  "customer_id": "CUST-12345",
  "interaction_mode": "interactive"
}
```

**Step 1 - Categorization:**
```
Category: Billing > Duplicate Charge
Priority: P2-High (financial impact)
Complexity: Moderate
Customer Name: Sarah Johnson
```

**Step 2 - Context:**
```
Account Status: Active (since 2022)
Tier: Enterprise
Previous Issues: None related to billing
Special Notes: Long-term customer, high value
```

**Step 3 - Diagnosis:**
```
Root Cause: System glitch during Dec 14 maintenance
Affected Accounts: 47 total
Confidence: High (pattern matches known issue)
```

**Step 4 - Resolution:**
```
Actions Taken:
- Refunded $29.99 duplicate charge
- Applied 1-month credit as goodwill
- Flagged for engineering review
```

**Step 5 - Documentation:**
```
Status: Resolved
Root Cause: System maintenance side effect
Tags: billing, duplicate-charge, dec-maintenance
Knowledge Base: Updated with resolution steps
```

**Step 6 - Follow-up:**
```
Response sent with personalized apology
7-day follow-up scheduled
Feedback request included
```

**Customer Response:**
```
Hi Sarah,

Thank you for bringing this to our attention. I've reviewed your account and
can confirm you were charged twice due to a system issue during our
December 14th maintenance window.

Here's what I've done for you:
- Refunded the duplicate charge of $29.99 (should appear in 3-5 business days)
- Applied a complimentary month to your account as an apology

I've also flagged this with our engineering team to ensure it doesn't happen
again. You're in good hands - this affected a small number of accounts and
is now resolved.

Is there anything else I can help you with today?

Best regards,
Support Team
```

### Example 2: Complex Technical Issue with Escalation

**Input:**
```json
{
  "ticket_content": "Our API integration has been failing intermittently for the past 3 days. Error: 'Connection timeout after 30000ms'. This is blocking our production deployment.",
  "customer_id": "CUST-67890",
  "priority_override": "P1",
  "interaction_mode": "auto"
}
```

**Process Summary:**
1. **Categorize**: Technical > API Integration, P1-Critical
2. **Context**: Enterprise customer, 50K API calls/day, no recent config changes
3. **Investigate**: Timeout correlates with peak traffic, regional latency detected
4. **Resolve/Escalate**: Escalated to Infrastructure with full diagnostics, provided temporary workaround (increased timeout + retry logic)
5. **Document**: Linked to infrastructure ticket, root cause pending
6. **Follow-up**: Committed to hourly updates until resolved

### Example 3: Feature Request Handling

**Input:**
```json
{
  "ticket_content": "It would be really helpful if we could export reports in PDF format instead of just CSV.",
  "customer_id": "CUST-11111",
  "interaction_mode": "interactive"
}
```

**Process Summary:**
1. **Categorize**: Product > Feature Request, P4-Low
2. **Context**: 3-year customer, heavy Analytics module user
3. **Investigate**: PDF export on roadmap for Q2, current workaround available
4. **Resolve**: Acknowledged, provided CSV-to-PDF workaround, added vote to feature
5. **Document**: Feature request logged with use case
6. **Follow-up**: Offered to notify when feature ships

## Troubleshooting

### Insufficient Ticket Information
If the ticket content is too vague to categorize or diagnose:
- You MUST NOT guess at the issue because incorrect assumptions lead to wrong solutions
- You SHOULD draft a friendly clarification request with specific questions
- You SHOULD provide a template for the customer to fill in

### Customer History Unavailable
If customer_id is not provided or lookup fails:
- You SHOULD proceed with available information while noting limitation
- You SHOULD ask the customer about relevant history
- You SHOULD flag in documentation that context was limited

### Ambiguous Escalation Decision
If it's unclear whether to escalate:
- You SHOULD default to attempting resolution first if within your capability
- In interactive mode, you SHOULD ask the user for guidance
- You MAY escalate for advisory without transferring ownership

### Unresponsive Customer
If the customer doesn't respond to follow-up:
- For P1/P2: Attempt multiple contact methods before closing
- For P3/P4: Send reminder and close after defined waiting period
- You MUST document all follow-up attempts

### Angry or Escalated Customer
If the customer is upset or demanding escalation:
- You MUST acknowledge their frustration empathetically
- You MUST NOT take complaints personally or become defensive
- You SHOULD focus on resolution rather than explanation
- You MAY offer immediate escalation if requested, with proper context

## Artifacts

All artifacts produced during the workflow:

- `categorization_summary`: Category, priority, complexity, initial assessment
- `customer_context`: Account status, history, patterns, special notes
- `diagnosis_report`: Symptoms, root cause, evidence, confidence level
- `resolution_action`: Action taken, response sent, escalation details
- `resolution_record`: Complete resolution documentation
- `closure_confirmation`: Final status, follow-up schedule, feedback
