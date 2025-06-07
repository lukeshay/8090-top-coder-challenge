#!/usr/bin/env python3

import json
import math
from collections import defaultdict

# Load the public cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Deep analysis of reimbursement patterns...\n")

# Let's test the basic per diem hypothesis
print("=== TESTING PER DIEM HYPOTHESIS ===")
print("Base hypothesis: $100/day + mileage + receipts adjustments")

for case in cases[:20]:  # Test first 20 cases
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    # Test simple formula: days * 100 + miles * 0.58
    simple_estimate = days * 100 + miles * 0.58
    mileage_component = miles * 0.58
    per_diem_component = days * 100
    receipt_effect = output - simple_estimate
    
    print(f"Days: {days}, Miles: {miles}, Receipts: ${receipts:.2f}")
    print(f"  Actual: ${output:.2f}")
    print(f"  Simple Est: ${simple_estimate:.2f} (${per_diem_component:.2f} per diem + ${mileage_component:.2f} mileage)")
    print(f"  Difference: ${output - simple_estimate:.2f} (likely receipt/bonus effect)")
    print()

print("\n=== ANALYZING MILEAGE TIERS ===")
# Group by mileage ranges to see if there are tiers
mileage_groups = defaultdict(list)
for case in cases:
    miles = case['input']['miles_traveled']
    days = case['input']['trip_duration_days']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    # Calculate dollars per mile (excluding per diem)
    estimated_per_diem = days * 100
    remaining = output - estimated_per_diem
    dollars_per_mile = remaining / miles if miles > 0 else 0
    
    if miles < 100:
        mileage_groups['0-99'].append(dollars_per_mile)
    elif miles < 200:
        mileage_groups['100-199'].append(dollars_per_mile)
    elif miles < 500:
        mileage_groups['200-499'].append(dollars_per_mile)
    elif miles < 1000:
        mileage_groups['500-999'].append(dollars_per_mile)
    else:
        mileage_groups['1000+'].append(dollars_per_mile)

print("Average $/mile after removing $100/day per diem:")
for range_name, values in mileage_groups.items():
    if values:
        avg = sum(values) / len(values)
        print(f"  {range_name} miles: ${avg:.3f}/mile (n={len(values)})")

print("\n=== TESTING 5-DAY BONUS HYPOTHESIS ===")
# Test Kevin's theory about 5-day trip bonuses
trip_duration_analysis = defaultdict(list)
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    # Simple baseline: $100/day + $0.58/mile
    baseline = days * 100 + miles * 0.58
    bonus = output - baseline
    
    trip_duration_analysis[days].append(bonus)

print("Average bonus/penalty by trip duration (vs $100/day + $0.58/mile):")
for days in sorted(trip_duration_analysis.keys()):
    bonuses = trip_duration_analysis[days]
    avg_bonus = sum(bonuses) / len(bonuses)
    print(f"  {days} days: ${avg_bonus:.2f} average bonus (n={len(bonuses)})")

print("\n=== EFFICIENCY ANALYSIS ===")
# Test miles per day efficiency hypothesis
efficiency_groups = defaultdict(list)
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    miles_per_day = miles / days if days > 0 else 0
    baseline = days * 100 + miles * 0.58
    bonus = output - baseline
    
    if miles_per_day < 50:
        efficiency_groups['0-49'].append(bonus)
    elif miles_per_day < 100:
        efficiency_groups['50-99'].append(bonus)
    elif miles_per_day < 150:
        efficiency_groups['100-149'].append(bonus)
    elif miles_per_day < 200:
        efficiency_groups['150-199'].append(bonus)
    elif miles_per_day < 250:
        efficiency_groups['200-249'].append(bonus)
    else:
        efficiency_groups['250+'].append(bonus)

print("Average bonus by miles per day:")
for range_name, bonuses in efficiency_groups.items():
    if bonuses:
        avg_bonus = sum(bonuses) / len(bonuses)
        print(f"  {range_name} miles/day: ${avg_bonus:.2f} average bonus (n={len(bonuses)})")

print("\n=== RECEIPTS ANALYSIS ===")
# Analyze receipt effects
receipt_groups = defaultdict(list)
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    receipts_per_day = receipts / days if days > 0 else 0
    baseline = days * 100 + miles * 0.58
    bonus = output - baseline
    
    if receipts_per_day < 50:
        receipt_groups['0-49/day'].append(bonus)
    elif receipts_per_day < 100:
        receipt_groups['50-99/day'].append(bonus)
    elif receipts_per_day < 200:
        receipt_groups['100-199/day'].append(bonus)
    elif receipts_per_day < 300:
        receipt_groups['200-299/day'].append(bonus)
    else:
        receipt_groups['300+/day'].append(bonus)

print("Average bonus by receipts per day:")
for range_name, bonuses in receipt_groups.items():
    if bonuses:
        avg_bonus = sum(bonuses) / len(bonuses)
        print(f"  ${range_name}: ${avg_bonus:.2f} average bonus (n={len(bonuses)})")

# Create better groups for incremental development
print("\n=== CREATING BETTER GROUPS ===")

# Group 1: Short trips, low complexity
group1 = []
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    
    if days <= 3 and miles <= 200 and receipts <= 100:
        group1.append(case)

# Group 2: Medium trips, medium complexity
group2 = []
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    
    if 4 <= days <= 7 and 200 < miles <= 800 and 100 < receipts <= 1000:
        group2.append(case)

# Group 3: Everything else
group3 = []
for case in cases:
    if case not in group1 and case not in group2:
        group3.append(case)

print(f"Group 1 (short/simple): {len(group1)} cases")
print(f"Group 2 (medium): {len(group2)} cases") 
print(f"Group 3 (complex/remaining): {len(group3)} cases")

# Save new groups
with open('groups/group1_short_simple.json', 'w') as f:
    json.dump(group1, f, indent=2)

with open('groups/group2_medium.json', 'w') as f:
    json.dump(group2, f, indent=2)

with open('groups/group3_complex.json', 'w') as f:
    json.dump(group3, f, indent=2)

print("Saved new groups to groups/ directory")