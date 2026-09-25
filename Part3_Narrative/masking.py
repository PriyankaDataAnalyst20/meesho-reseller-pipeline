def alias_for(reseller_id):
    """
    Convert reseller_id to safe alias format.
    
    Example:
        alias_for("RS019") → "ALIAS-19"
        alias_for("RS024") → "ALIAS-24"
    """
    number = reseller_id.replace("RS", "")
    return f"ALIAS-{int(number)}"


def assert_no_raw_names_leak(text, reseller_names):
    """
    Check if any raw reseller names appear in text.
    
    Args:
        text: Narrative text to check
        reseller_names: List of raw reseller names
    
    Returns:
        bool: False if any name leaked, True if clean
    """
    for name in reseller_names:
        if name in text:
            return False
    return True


# Test the functions
if __name__ == "__main__":
    print("="*60)
    print("PART 3: Masking Tests")
    print("="*60)
    
    print("\nTest 1: Alias conversion")
    assert alias_for("RS019") == "ALIAS-19"
    assert alias_for("RS024") == "ALIAS-24"
    print("✓ Passed")
    
    print("\nTest 2: Name leak detection - safe text")
    safe_text = "ALIAS-19 showed strong growth in May"
    names = ["Mumbai Reseller 1", "Delhi Reseller 2"]
    assert assert_no_raw_names_leak(safe_text, names) == True
    print("✓ Passed")
    
    print("\nTest 3: Name leak detection - leaked text")
    leaked_text = "Mumbai Reseller 1 showed strong growth"
    assert assert_no_raw_names_leak(leaked_text, names) == False
    print("✓ Passed")
    
    # Top Reseller Narrative Test
    print("\nTest 4: Top-reseller narrative (safe version)")
    top_reseller_names = [
        "Mumbai Reseller 1",
        "Bangalore Reseller 2", 
        "Delhi Reseller 3",
        "Chennai Reseller 4",
        "Kolkata Reseller 5"
    ]
    
    safe_narrative = f"""
    North region {alias_for("RS019")} led revenue generation with ₹75,295.09 across all categories.
    This top performer showed consistent growth patterns and warrants recognition in 
    the monthly business review. Consider this reseller for pilot testing of new category promotions.
    """
    
    assert assert_no_raw_names_leak(safe_narrative, top_reseller_names) == True
    print("✓ Passed - No raw names leaked")
    
    print("\nTest 5: Top-reseller narrative (leaked version - should fail)")
    leaked_narrative = f"""
    Mumbai Reseller 1 led revenue generation with ₹75,295.09 across all categories.
    This top performer showed consistent growth patterns and warrants recognition.
    """
    
    assert assert_no_raw_names_leak(leaked_narrative, top_reseller_names) == False
    print("✓ Passed - Leak correctly detected")
    
    print("\n" + "="*60)
    print("✅ All masking tests passed!")
    print("="*60)