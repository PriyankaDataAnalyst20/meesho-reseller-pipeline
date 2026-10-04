MEESHO RESELLER GROWTH AND ALERT INTELLIGENCE PIPELINE

SECTION 1: HOW TO REGENERATE DATASET AND RUN EVERY PART IN ORDER

Step 1: Regenerate Dataset
cd data
python generate_dataset.py
Creates resellers.csv, orders.csv, meesho_reseller.db (seed=42). Total: 24 resellers, 900 orders.

Step 2: Run Part 1 - SQL Analytics
cd part1_sql
python queries.py
Outputs 7 CSV files with monthly revenue, regions, top resellers, totals.

Step 3: Run Part 2 - Growth Detection
cd part2_engine
python test_growth_engine.py
All 13 tests pass. Validates Mom growth and flagging logic.

Step 4: Review Part 3 - Narrative and Masking
Read prompt_pack.md, narrative_report.md, masking.py files (no execution needed).

Step 5: Run Part 4 - Agent Orchestration
cd part4_agent
python mock_agent_runner.py
Outputs JSON for May (valid), June (valid), Corrupted feed (invalid).

SECTION 2: ZERO API KEYS REQUIRED

This pipeline runs entirely locally with NO external dependencies:
- No Gmail or Slack sending
- No database connections
- No authentication tokens
- No API keys for any service
- All data generated locally, deterministic, offline

Clone repo and run the commands above. Everything works without internet.

SECTION 3: WORKFLOW PATTERNS FOR PARTS 1, 2, 3

Part 1 SQL Analytics
Pattern: Raw Data Intake → Structured Aggregation
Reads 900 orders, computes 15 monthly revenues via SQL GROUP BY, outputs verified numbers.

Part 2 Growth Detection Engine
Pattern: Compute Real Numbers via SQL First, Then Hand Off to Python Business Logic
Takes Part 1 output, calculates Mom percentages, applies 8% threshold flagging, validates inputs.

Part 3 Narrative and Masking
Pattern: Template Fill then Privacy Protection
Takes flagged facts from Part 2, fills Context+Insight+Implication template, masks reseller names (RS019 → ALIAS-19).

SECTION 4: WORKFLOW PATTERN FOR PART 4

Part 4 Agent Orchestration
Pattern: Intake → Summary → Report Draft → Validate
Step 1 Intake: Load monthly CSV feed
Step 2 Summary: Validate feed via Part 2 validate_feed (hard stop if invalid)
Step 3 Report Draft: Compute Mom for all categories, flag top 3, suppress rest
Step 4 Validate: Output JSON with drafts marked for human approval (no auto-send)

