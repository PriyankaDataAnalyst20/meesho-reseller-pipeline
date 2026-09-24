def mom_growth(previous, current):
    """Calculate Month-on-Month growth %"""
    if previous == 0:
        return 0.0
    growth = ((current - previous) / previous) * 100
    return round(growth, 2)


def is_flagged(mom_pct, threshold=8.0):
    """Return flagged/not_flagged/escalate_exact_boundary"""
    abs_pct = abs(mom_pct)
    if abs_pct > threshold:
        return "flagged"
    elif abs_pct < threshold:
        return "not_flagged"
    else:
        return "escalate_exact_boundary"


def validate_feed(csv_path):
    """Validate CSV feed and return (is_valid, errors_list)"""
    import csv
    import os
    
    errors = []
    
    if not os.path.exists(csv_path):
        return (False, [f"File not found: {csv_path}"])
    
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            
            for line_num, row in enumerate(reader, start=2):
                month = row.get('month', '').strip()
                category = row.get('category', '').strip()
                revenue = row.get('revenue', '').strip()
                
                # Check missing category
                if not category:
                    errors.append(f"line {line_num}: missing category (month={month})")
                
                # Check missing revenue
                if not revenue:
                    errors.append(f"line {line_num}: missing revenue (category={category})")
                    continue
                
                # Check revenue is numeric
                try:
                    revenue_float = float(revenue)
                except ValueError:
                    errors.append(f"line {line_num}: revenue not numeric: {revenue!r}")
                    continue
                
                # Check negative revenue
                if revenue_float < 0:
                    errors.append(f"line {line_num}: negative revenue ({revenue_float}) for category={category}")
        
        return (len(errors) == 0, errors)
    
    except Exception as e:
        return (False, [f"Error reading file: {str(e)}"])