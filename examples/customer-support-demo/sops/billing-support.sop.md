# Billing Support

## Overview

Resolve billing support tickets with a 3-step workflow: Understand → Resolve → Confirm.

**You MUST follow these steps in order and produce the specified output for each step.**

## Parameters

- **ticket** (required): The customer's billing-related message or complaint

## Steps

### 1. Understand

Analyze the ticket and list ALL issues before attempting any resolution.

**Constraints:**
- You MUST use the `categorize_ticket` tool to classify the issue type and priority
- You MUST use the `customer_lookup` tool to get customer context (if customer_id available)
- You MUST output a numbered list of every distinct issue in the ticket
- You MUST NOT skip this step or combine it with resolution
- You MUST NOT attempt to resolve anything until all issues are listed

**Required Output Format:**
```
## Issues Identified
1. [Issue type]: [Description]
2. [Issue type]: [Description]
...
```

### 2. Resolve

Address EACH identified issue with a specific action.

**Constraints:**
- You MUST use `search_knowledge_base` tool to find relevant solutions
- You MUST address EVERY issue from Step 1 - do not skip any
- You MUST state the specific action taken for each issue
- You MUST include concrete details (amounts, dates, timelines)
- You SHOULD offer goodwill compensation for company errors

**Required Output Format:**
```
## Actions Taken
1. [Issue]: [Action + Details]
2. [Issue]: [Action + Details]
...
```

### 3. Confirm

Summarize and verify completeness.

**Constraints:**
- You MUST provide a checklist showing each issue is addressed
- You MUST ask if all concerns have been resolved
- You MUST invite follow-up questions

**Required Output Format:**
```
## Summary
- [x] Issue 1: [Status]
- [x] Issue 2: [Status]
...

All issues addressed? Please let me know if anything was missed.
```
