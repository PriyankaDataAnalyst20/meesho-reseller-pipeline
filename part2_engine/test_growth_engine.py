from growth_engine import mom_growth, is_flagged, validate_feed

print("="*60)
print("PART 2: Growth Engine Tests")
print("="*60)

# Test 1: Ethnic Wear April→May (77.1%, flagged)
print("\nTest 1: Ethnic Wear April→May")
g = mom_growth(104520.77, 185107.61)
f = is_flagged(g)
assert g == 77.1, f"Expected 77.1, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ 77.1% = {f}")

# Test 2: Western Wear April→May (-23.6%, flagged)
print("Test 2: Western Wear April→May")
g = mom_growth(113866.15, 86998.18)
f = is_flagged(g)
assert g == -23.6, f"Expected -23.6, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ -23.6% = {f}")

# Test 3: Kids Wear April→May (-23.48%, flagged)
print("Test 3: Kids Wear April→May")
g = mom_growth(59847.27, 45793.78)
f = is_flagged(g)
assert g == -23.48, f"Expected -23.48, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ -23.48% = {f}")

# Test 4: Home & Kitchen April→May (-9.25%, flagged)
print("Test 4: Home & Kitchen April→May")
g = mom_growth(100446.23, 91152.57)
f = is_flagged(g)
assert g == -9.25, f"Expected -9.25, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ -9.25% = {f}")

# Test 5: Beauty April→May (-12.75%, flagged)
print("Test 5: Beauty & Personal Care April→May")
g = mom_growth(40737.01, 35542.11)
f = is_flagged(g)
assert g == -12.75, f"Expected -12.75, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ -12.75% = {f}")

# Test 6: Ethnic Wear May→June (-58.74%, flagged)
print("Test 6: Ethnic Wear May→June")
g = mom_growth(185107.61, 76371.53)
f = is_flagged(g)
assert g == -58.74, f"Expected -58.74, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ -58.74% = {f}")

# Test 7: Western Wear May→June (11.97%, flagged)
print("Test 7: Western Wear May→June")
g = mom_growth(86998.18, 97415.64)
f = is_flagged(g)
assert g == 11.97, f"Expected 11.97, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ 11.97% = {f}")

# Test 8: Kids Wear May→June (23.9%, flagged)
print("Test 8: Kids Wear May→June")
g = mom_growth(45793.78, 56737.78)
f = is_flagged(g)
assert g == 23.9, f"Expected 23.9, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ 23.9% = {f}")

# Test 9: Home & Kitchen May→June (42.59%, flagged)
print("Test 9: Home & Kitchen May→June")
g = mom_growth(91152.57, 129971.22)
f = is_flagged(g)
assert g == 42.59, f"Expected 42.59, got {g}"
assert f == "flagged", f"Expected 'flagged', got {f}"
print(f"  ✓ 42.59% = {f}")

# Test 10: Beauty May→June (5.67%, not_flagged)
print("Test 10: Beauty & Personal Care May→June")
g = mom_growth(35542.11, 37559.07)
f = is_flagged(g)
assert g == 5.67, f"Expected 5.67, got {g}"
assert f == "not_flagged", f"Expected 'not_flagged', got {f}"
print(f"  ✓ 5.67% = {f}")

# Test 11: Boundary case (8.0%, escalate_exact_boundary)
print("Test 11: Boundary case 8.0%")
g = mom_growth(100000, 108000)
f = is_flagged(g)
assert g == 8.0, f"Expected 8.0, got {g}"
assert f == "escalate_exact_boundary", f"Expected 'escalate_exact_boundary', got {f}"
print(f"  ✓ 8.0% = {f}")

# Test 12: Corrupted feed validation
print("Test 12: Corrupted feed validation")
is_valid, errors = validate_feed("part2_engine/fixtures/corrupted_feed.csv")
assert is_valid == False, f"Expected invalid, got {is_valid}"
assert len(errors) == 3, f"Expected 3 errors, got {len(errors)}: {errors}"
assert errors[0] == "line 3: negative revenue (-4200.0) for category=Western Wear", f"Error 1 mismatch: {errors[0]}"
assert errors[1] == "line 4: missing category (month=July)", f"Error 2 mismatch: {errors[1]}"
assert errors[2] == "line 6: missing revenue (category=Home & Kitchen)", f"Error 3 mismatch: {errors[2]}"
print(f"  ✓ 3 errors detected in correct order")

# Test 13: Valid feed validation
print("Test 13: Valid feed validation")
is_valid, errors = validate_feed("part2_engine/fixtures/monthly_category_revenue.csv")
assert is_valid == True, f"Expected valid, got {is_valid}"
assert len(errors) == 0, f"Expected 0 errors, got {len(errors)}: {errors}"
print(f"  ✓ All 15 rows valid")

print("\n" + "="*60)
print("✅ ALL 13 TESTS PASSED!")
print("="*60)