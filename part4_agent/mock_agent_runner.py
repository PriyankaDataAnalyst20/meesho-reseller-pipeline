import csv
import json
import os
import sys

sys.path.insert(0, '.')
from part2_engine.growth_engine import mom_growth, is_flagged, validate_feed


def load_monthly_data(csv_path, month_filter):
    """Load revenue data from CSV for a specific month"""
    data = {}
    if not os.path.exists(csv_path):
        return None
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                month = row.get('month', '').strip()
                category = row.get('category', '').strip()
                revenue_str = row.get('revenue', '').strip()
                
                if month == month_filter and category and revenue_str:
                    revenue = float(revenue_str)
                    data[category] = revenue
    except Exception as e:
        return None
    return data if data else None


def prompt_pack_fill(category, month, prev_month, previous_revenue, current_revenue, mom_pct):
    """Fill narrative template"""
    context = f"{category} revenue in {month} was ₹{current_revenue} compared to ₹{previous_revenue} in {prev_month}."
    
    if mom_pct > 0:
        insight = f"This represents a {mom_pct}% increase month-on-month, indicating strong growth."
    else:
        insight = f"This represents a {mom_pct}% decline month-on-month, signaling a reversal."
    
    if mom_pct > 0:
        implication = f"Investigate drivers and sustain momentum."
    else:
        implication = f"Review market conditions and pricing strategy."
    
    return f"{context} {insight} {implication}"


def run(month, prev_month_name, previous_month_csv, current_month_csv):
    """Run agent for one month"""
    
    is_valid, errors = validate_feed(current_month_csv)
    if not is_valid:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": errors,
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }
    
    prev_data = load_monthly_data(previous_month_csv, prev_month_name)
    curr_data = load_monthly_data(current_month_csv, month)
    
    if not prev_data or not curr_data:
        return {
            "run_month": month,
            "validation_status": "invalid",
            "validation_errors": ["Failed to load month data"],
            "flagged_categories": [],
            "suppressed_categories": [],
            "escalated_categories": [],
            "action_taken": "hard_stop"
        }
    
    all_results = []
    for category in curr_data:
        if category in prev_data:
            prev_rev = prev_data[category]
            curr_rev = curr_data[category]
            growth = mom_growth(prev_rev, curr_rev)
            flag = is_flagged(growth)
            
            all_results.append({
                "category": category,
                "mom_pct": growth,
                "previous_revenue": prev_rev,
                "current_revenue": curr_rev,
                "flag_status": flag
            })
    
    flagged = [r for r in all_results if r["flag_status"] == "flagged"]
    escalated = [r for r in all_results if r["flag_status"] == "escalate_exact_boundary"]
    flagged.sort(key=lambda x: abs(x["mom_pct"]), reverse=True)
    
    drafted = []
    suppressed = []
    
    for i, r in enumerate(flagged):
        if i < 3:
            msg = prompt_pack_fill(r["category"], month, prev_month_name, r["previous_revenue"], r["current_revenue"], r["mom_pct"])
            drafted.append({
                "category": r["category"],
                "mom_pct": r["mom_pct"],
                "previous_revenue": r["previous_revenue"],
                "current_revenue": r["current_revenue"],
                "drafted": True,
                "message": msg
            })
        else:
            suppressed.append(r["category"])
    
    escalated_names = [r["category"] for r in escalated]
    
    return {
        "run_month": month,
        "validation_status": "valid",
        "validation_errors": [],
        "flagged_categories": drafted,
        "suppressed_categories": suppressed,
        "escalated_categories": escalated_names,
        "action_taken": "drafted_and_held_for_approval"
    }


if __name__ == "__main__":
    import os
    
    print("="*60)
    print("PART 4: Mock Agent Runner")
    print("="*60)
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(base_dir)
    
    csv_file = os.path.join(root_dir, "part2_engine/fixtures/monthly_category_revenue.csv")
    corrupted_file = os.path.join(root_dir, "part2_engine/fixtures/corrupted_feed.csv")
    
    print(f"\nUsing CSV: {csv_file}")
    print(f"Using Corrupted: {corrupted_file}\n")
    
    print("--- May Scenario (April -> May) ---")
    r1 = run("May", "April", csv_file, csv_file)
    print(json.dumps(r1, indent=2))
    
    print("\n--- June Scenario (May -> June) ---")
    r2 = run("June", "May", csv_file, csv_file)
    print(json.dumps(r2, indent=2))
    
    print("\n--- Corrupted Feed Scenario ---")
    r3 = run("July", "June", csv_file, corrupted_file)
    print(json.dumps(r3, indent=2))
    
    print("\n" + "="*60)
    print("Agent run complete")
    print("="*60)