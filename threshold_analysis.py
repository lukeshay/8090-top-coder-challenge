#!/usr/bin/env python3

import json

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

# Extract 1-day trips for detailed analysis
one_day_cases = [case for case in cases if case['input']['trip_duration_days'] == 1]

print(f"Analyzing {len(one_day_cases)} one-day trips for thresholds")

# Sort by receipt amount to find thresholds
one_day_cases.sort(key=lambda x: x['input']['total_receipts_amount'])

print("\nReceipt threshold analysis (sorted by receipt amount):")
print("Receipts | Miles | Expected | Receipt Ratio | Effective Receipt Rate")
print("---------|-------|----------|---------------|----------------------")

for case in one_day_cases:
    inp = case['input']
    expected = case['expected_output']
    
    # Calculate what portion seems to come from receipts
    # Assume base ~50 and mileage at ~0.5/mile for rough estimate
    estimated_base_and_mileage = 50 + inp['miles_traveled'] * 0.5
    receipt_contribution = expected - estimated_base_and_mileage
    receipt_ratio = receipt_contribution / inp['total_receipts_amount'] if inp['total_receipts_amount'] > 0 else 0
    
    simple_ratio = expected / inp['total_receipts_amount'] if inp['total_receipts_amount'] > 0 else 0
    
    print(f"${inp['total_receipts_amount']:7.2f} | {inp['miles_traveled']:5.0f} | ${expected:8.2f} | {simple_ratio:11.3f} | {receipt_ratio:17.3f}")

print("\n" + "="*80)

# Sort by mileage to find mileage thresholds  
one_day_cases.sort(key=lambda x: x['input']['miles_traveled'])

print("\nMileage threshold analysis (sorted by miles):")
print("Miles | Receipts | Expected | Per Mile | Effective Mile Rate")
print("------|----------|----------|----------|-------------------")

for case in one_day_cases:
    inp = case['input']
    expected = case['expected_output']
    
    per_mile = expected / inp['miles_traveled'] if inp['miles_traveled'] > 0 else 0
    
    # Calculate effective mileage rate (subtract estimated base and receipts)
    estimated_base_and_receipts = 50 + inp['total_receipts_amount'] * 0.3  # rough estimate
    mile_contribution = expected - estimated_base_and_receipts
    effective_mile_rate = mile_contribution / inp['miles_traveled'] if inp['miles_traveled'] > 0 else 0
    
    print(f"{inp['miles_traveled']:5.0f} | ${inp['total_receipts_amount']:7.2f} | ${expected:8.2f} | ${per_mile:6.3f} | ${effective_mile_rate:15.3f}")

print("\n" + "="*80)

# Look for specific patterns around suspected thresholds
print("\nLooking for specific threshold patterns:")

# Cases around $400-600 receipts
print("\nCases with receipts around $400-600:")
for case in one_day_cases:
    inp = case['input']
    if 400 <= inp['total_receipts_amount'] <= 600:
        expected = case['expected_output']
        ratio = expected / inp['total_receipts_amount']
        print(f"  ${inp['total_receipts_amount']:6.2f} receipts, {inp['miles_traveled']:3.0f} miles → ${expected:7.2f} (ratio: {ratio:.3f})")

# Cases around 400-600 miles
print("\nCases with miles around 400-600:")
for case in one_day_cases:
    inp = case['input']
    if 400 <= inp['miles_traveled'] <= 600:
        expected = case['expected_output']
        per_mile = expected / inp['miles_traveled']
        print(f"  {inp['miles_traveled']:3.0f} miles, ${inp['total_receipts_amount']:6.2f} receipts → ${expected:7.2f} (per mile: ${per_mile:.3f})")

# Try to identify the calculation for low receipt, low mileage cases
print("\nLow receipt (<$50), low mileage (<200) cases:")
low_cases = [case for case in one_day_cases if case['input']['total_receipts_amount'] < 50 and case['input']['miles_traveled'] < 200]

for case in low_cases:
    inp = case['input']
    expected = case['expected_output']
    
    # Try different base assumptions
    for base in [50, 70, 90, 100, 110]:
        remainder = expected - base
        if remainder > 0:
            implied_mile_rate = (remainder - inp['total_receipts_amount']) / inp['miles_traveled'] if inp['miles_traveled'] > 0 else 0
            if 0.5 <= implied_mile_rate <= 0.7:  # Reasonable range
                print(f"  {inp['miles_traveled']:3.0f} miles, ${inp['total_receipts_amount']:5.2f} receipts → ${expected:7.2f}")
                print(f"    Base ${base} → Mile rate: ${implied_mile_rate:.3f}")
                break 