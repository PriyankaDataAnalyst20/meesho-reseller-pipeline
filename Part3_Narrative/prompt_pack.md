# Prompt Pack: Flagged Category Narrative Template

## Trigger

This prompt pack activates when:
- A category's `is_flagged()` function returns `"flagged"` (absolute MoM growth > 8%)
- A stakeholder-ready narrative is needed for regional manager review
- The category requires business justification before action or escalation

## Purpose
Convert flagged category data into stakeholder-ready narratives that explain what happened and what to do next.

## Template Structure

Every narrative follows: **Context → Insight → Implication**

### Input Variables
- `{month}` - Current month (e.g., May)
- `{prev_month}` - Previous month (e.g., April)
- `{category}` - Product category (e.g., Ethnic Wear)
- `{previous_revenue}` - Revenue in previous month
- `{current_revenue}` - Revenue in current month
- `{mom_pct}` - Month-on-Month growth percentage

### Narrative Template

CONTEXT
"{category} revenue in {month} was ₹{current_revenue} compared to ₹{previous_revenue} in {prev_month}."

INSIGHT
"This represents a {mom_pct}% change month-on-month. [If positive: Strong growth signals] [If negative: Significant decline requires attention]."

IMPLICATION
"[If flagged positive] Investigate success drivers and develop strategies to sustain momentum. [If flagged negative] Review market conditions, pricing, and promotions to identify recovery opportunities."


## Validation Checklist 

Does every number in the draft match a supplied placeholder value exactly?
Is every claim labeled as fact or hypothesis?
Is the recommendation specific and actionable, not vague?
Is any reseller referenced only by coded alias (ALIAS-XX), never by raw name?


## Example Narratives (See narrative_report.md)

1. May Ethnic Wear: +77.1% growth (flagged)
2. June Ethnic Wear: -58.74% decline (flagged)