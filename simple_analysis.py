#!/usr/bin/env python3

import json

# Load the simple group
with open('groups/group1_short_simple.json', 'r') as f:
    cases = json.load(f)

print("ANALYZING SIMPLE GROUP TO FIND BASIC FORMULA")
print("=" * 50)

for i, case in enumerate(cases):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    print(f"\nCase {i+1}:")
    print(f"  Days: {days}, Miles: {miles}, Receipts: ${receipts:.2f}")
    print(f"  Expected: ${output:.2f}")
    
    # Test different per diem rates
    per_diem_100 = days * 100
    per_diem_120 = days * 120
    per_diem_130 = days * 130
    
    # Test different mileage rates
    mileage_58 = miles * 0.58
    mileage_50 = miles * 0.50
    mileage_65 = miles * 0.65
    mileage_70 = miles * 0.70
    mileage_75 = miles * 0.75
    mileage_80 = miles * 0.80
    mileage_100 = miles * 1.0
    mileage_120 = miles * 1.2
    mileage_150 = miles * 1.5
    mileage_200 = miles * 2.0
    
    print(f"  Per diem $100: ${per_diem_100:.2f}")
    print(f"  Per diem $120: ${per_diem_120:.2f}")
    print(f"  Per diem $130: ${per_diem_130:.2f}")
    
    print(f"  Mileage $0.58: ${mileage_58:.2f}")
    print(f"  Mileage $0.65: ${mileage_65:.2f}")
    print(f"  Mileage $0.80: ${mileage_80:.2f}")
    print(f"  Mileage $1.20: ${mileage_120:.2f}")
    print(f"  Mileage $2.00: ${mileage_200:.2f}")
    
    # Test some combinations
    combo1 = per_diem_100 + mileage_58  # Standard assumption
    combo2 = per_diem_120 + mileage_65
    combo3 = per_diem_120 + mileage_200
    combo4 = per_diem_130 + mileage_150
    
    print(f"  Combo 1 ($100/day + $0.58/mile): ${combo1:.2f} (diff: ${abs(output - combo1):.2f})")
    print(f"  Combo 2 ($120/day + $0.65/mile): ${combo2:.2f} (diff: ${abs(output - combo2):.2f})")
    print(f"  Combo 3 ($120/day + $2.00/mile): ${combo3:.2f} (diff: ${abs(output - combo3):.2f})")
    print(f"  Combo 4 ($130/day + $1.50/mile): ${combo4:.2f} (diff: ${abs(output - combo4):.2f})")
    
    # What if receipts add directly?
    combo_with_receipts = combo1 + receipts
    print(f"  Combo 1 + receipts: ${combo_with_receipts:.2f} (diff: ${abs(output - combo_with_receipts):.2f})")

print("\n\nLOOKING FOR PATTERNS:")
print("=" * 30)

best_diffs = []
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    # Try the combo that seems to work best: $120/day + $2.00/mile
    estimate = days * 120 + miles * 2.0
    diff = output - estimate
    best_diffs.append(diff)
    
    print(f"Days: {days}, Miles: {miles}, Receipts: ${receipts:.2f}")
    print(f"  Expected: ${output:.2f}, Est: ${estimate:.2f}, Diff: ${diff:.2f}")

print(f"\nAverage difference: ${sum(best_diffs)/len(best_diffs):.2f}")
print(f"This suggests: Base = $120/day + $2.00/mile + small adjustments")