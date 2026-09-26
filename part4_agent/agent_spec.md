# Agent Specification: Meesho Category Monitoring Agent

## Goal

Keep Meesho category managers informed of any product category whose month-on-month revenue moves beyond the 8% threshold, with a human approving every drafted message before it is considered sent.

---

## Tools

The agent calls these concrete functions (imported from Part 2 and Part 3):

- validate_feed(csv_path) - Validates input CSV for missing/negative/non-numeric values
- mom_growth(previous, current) - Calculates Month-on-Month growth percentage
- is_flagged(mom_pct, threshold=8.0) - Classifies growth as "flagged", "not_flagged", or "escalate_exact_boundary"
- prompt_pack_template(category, month, prev_month, previous_revenue, current_revenue, mom_pct) - Fills the Part 3 prompt template into a narrative draft

---

## Memory/State

Between runs, the agent must retain:

- Previous month's revenue per category (e.g., April: Ethnic Wear: 104520.77, Western Wear: 113866.15, ...)
- Current month's revenue per category (e.g., May: Ethnic Wear: 185107.61, ...)
- List of categories already reported in prior months (to avoid duplicate notifications)
- Threshold setting (8.0%)

---

## Planner

The agent executes 8 ordered subtasks:

1. Load the current-month revenue feed and run validate_feed
2. If invalid, Hard Stop and report all validation errors
3. If valid, compute mom_growth for every category against the previous month
4. Run is_flagged on every category result
5. Sort all flagged categories by abs(mom_pct) in descending order
6. Draft a message (via Part 3 template) for the top 3 flagged categories by magnitude
7. Log any remaining flagged categories (4th onward) as suppressed, without drafting
7b. Separately log any category with is_flagged = "escalate_exact_boundary" into escalated_categories
8. Emit one structured JSON object summarizing the run

---

## Feedback Loop

Human Approval Checkpoint:

Every drafted message is held for human review before any "send" action (simulated as a flag in the JSON output: action_taken = "drafted_and_held_for_approval"). No message is auto-sent. The human can approve, edit, or reject each draft. This simulated approval is indicated in the JSON, not by actual email transmission.

---

## Input / Action / Output Guardrails

Input Guardrail:
validate_feed must return (True, []) before any other computation proceeds. If it returns (False, errors), execution stops and errors are surfaced immediately.

Action Guardrail:
No message is ever automatically sent. All drafted messages are held in the JSON output with drafted = true and a message string, awaiting human approval.

Output Guardrail:
Every numeric value in a drafted message (revenue figures, percentages, dates) must trace directly to Part 1 SQL output or Part 2 mom_growth computation. No invented figures. Every number is verifiable.

---

## Success and Error Stopping Conditions

Success:
validation_status = "valid" and action_taken = "drafted_and_held_for_approval"
Drafts are produced for flagged categories (or zero drafts if nothing crossed the 8% threshold)
Every number in every drafted message is traceable to Part 1/Part 2 data
Suppressed and escalated categories are logged but not drafted

Error - Hard Stop:
validation_status = "invalid" and action_taken = "hard_stop"
validate_feed returned False with errors
No MoM computation is attempted
validation_errors list is populated with all error messages from validate_feed
flagged_categories, suppressed_categories, escalated_categories are all empty

---

## Given-When-Then Specifications (4 Agent-Level Specs)

Spec 1: May Ethnic Wear Spike
GIVEN April Ethnic Wear revenue of ₹104,520.77 and May revenue of ₹185,107.61, WHEN the agent computes MoM and evaluates, THEN mom_growth returns 77.1 and is_flagged returns "flagged", triggering a drafted message with category=Ethnic Wear, mom_pct=77.1.

Spec 2: June Beauty Slight Rise
GIVEN May Beauty & Personal Care revenue of ₹35,542.11 and June revenue of ₹37,559.07, WHEN the agent computes MoM and evaluates, THEN mom_growth returns 5.67 and is_flagged returns "not_flagged", so no message is drafted for this category.

Spec 3: Boundary Case (8.0% Exactly)
GIVEN a synthetic previous month revenue of 100000 and current revenue of 108000, WHEN the agent computes MoM, THEN mom_growth returns 8.0 exactly and is_flagged returns "escalate_exact_boundary", placing this category in escalated_categories (no draft, held for manual review).

Spec 4: Corrupted Feed Hard Stop
GIVEN a CSV with missing category, negative revenue, and missing revenue fields (part2_engine/fixtures/corrupted_feed.csv), WHEN the agent runs validate_feed, THEN it returns (False, [3 errors]), action_taken becomes "hard_stop", and no MoM computation is attempted.

---

## Ordered Subtasks (Planner Detail)

See part4_agent/mock_agent_runner.py for implementation of these 8 subtasks.
