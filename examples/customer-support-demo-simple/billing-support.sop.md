# Billing Support

## Overview

Handle billing inquiries with a 3-step workflow: Understand → Resolve → Confirm.

**You MUST follow these steps in order and produce the specified output for each step.**

## Parameters

- **ticket** (required): The customer's billing-related message or complaint

## Steps

### 1. Understand

Analyze the ticket and list ALL issues before attempting any resolution.

**Constraints:**
- You MUST output a numbered list of every distinct issue in the ticket
- You MUST NOT skip this step or combine it with resolution
- You MUST NOT attempt to resolve anything until all issues are listed
- You MUST categorize each issue (billing error, refund request, plan change, question, etc.)

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
- [ ] Issue 1: [Status]
- [ ] Issue 2: [Status]
...

All issues addressed? Please let me know if anything was missed.
```

## Example

**Input:**
```
I need to upgrade to Pro AND add 2 more team seats. Also is there a discount for annual billing?
```

**Expected Output:**
```
## Issues Identified
1. Plan change: Upgrade to Pro plan requested
2. Account modification: Add 2 team seats
3. Question: Annual billing discount inquiry

## Actions Taken
1. Pro upgrade: Upgraded your account to Pro ($29.99/mo), effective immediately
2. Team seats: Added 2 seats ($10/seat/mo = $20/mo additional)
3. Annual discount: Yes! 20% off with annual billing - would you like to switch?

## Summary
- [x] Pro upgrade: Complete
- [x] Team seats: 2 added
- [x] Annual discount: Information provided

All issues addressed? Please let me know if anything was missed or if you have other questions!
```
