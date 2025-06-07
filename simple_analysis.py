#!/usr/bin/env python3

import json

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

# Extract 1-day trips for detailed analysis
one_day_cases = [case for case in cases if case['input']['trip_duration_days'] == 1]

print(f"Analyzing {len(one_day_cases)} one-day trips")

# Analyze some patterns
print("\nFirst 20 one-day cases:")
print("Miles | Receipts | Expected | Miles*0.58+Rcpts | Diff")
print("------|----------|----------|------------------|-----")

for case in one_day_cases[:20]:
    inp = case['input']
    expected = case['expected_output']
    
    # Simple calculation: miles * 0.58 + receipts
    simple_calc = inp['miles_traveled'] * 0.58 + inp['total_receipts_amount']
    diff = expected - simple_calc
    
    print(f"{inp['miles_traveled']:5.0f} | ${inp['total_receipts_amount']:7.2f} | ${expected:8.2f} | ${simple_calc:15.2f} | ${diff:5.2f}")

# Look for a base amount pattern
print("\nTrying to find base amount pattern:")
base_amounts = []
for case in one_day_cases[:20]:
    inp = case['input']
    expected = case['expected_output']
    
    # What would be the base if we subtract simple mileage and receipts?
    base = expected - inp['miles_traveled'] * 0.58 - inp['total_receipts_amount']
    base_amounts.append(base)
    print(f"Miles: {inp['miles_traveled']:3.0f}, Receipts: ${inp['total_receipts_amount']:6.2f}, Expected: ${expected:7.2f}, Implied base: ${base:6.2f}")

avg_base = sum(base_amounts) / len(base_amounts)
print(f"\nAverage implied base: ${avg_base:.2f}")

# Check high mileage cases
print("\nHigh mileage cases (>300 miles):")
high_mileage = [case for case in one_day_cases if case['input']['miles_traveled'] > 300]
for case in high_mileage[:10]:
    inp = case['input']
    expected = case['expected_output']
    
    # Try to understand effective rate
    total_per_mile = expected / inp['miles_traveled']
    effective_miles_rate = (expected - inp['total_receipts_amount']) / inp['miles_traveled']
    
    print(f"  {inp['miles_traveled']:3.0f} miles, ${inp['total_receipts_amount']:6.2f} receipts → ${expected:7.2f}")
    print(f"    Total per mile: ${total_per_mile:.4f}, Effective miles rate: ${effective_miles_rate:.4f}")

# Check high receipt cases
print("\nHigh receipt cases (>$500):")
high_receipts = [case for case in one_day_cases if case['input']['total_receipts_amount'] > 500]
for case in high_receipts[:10]:
    inp = case['input']
    expected = case['expected_output']
    
    receipt_ratio = expected / inp['total_receipts_amount']
    miles_contribution = inp['miles_traveled'] * 0.58
    receipt_contribution = expected - miles_contribution
    
    print(f"  {inp['miles_traveled']:3.0f} miles, ${inp['total_receipts_amount']:6.2f} receipts → ${expected:7.2f}")
    print(f"    Receipt ratio: {receipt_ratio:.3f}, Miles contrib: ${miles_contribution:.2f}, Receipt contrib: ${receipt_contribution:.2f}")

# Simple statistical analysis
print(f"\nSimple statistics for 1-day trips:")
miles_values = [case['input']['miles_traveled'] for case in one_day_cases]
receipt_values = [case['input']['total_receipts_amount'] for case in one_day_cases]
output_values = [case['expected_output'] for case in one_day_cases]

print(f"Miles - Min: {min(miles_values):.0f}, Max: {max(miles_values):.0f}, Avg: {sum(miles_values)/len(miles_values):.1f}")
print(f"Receipts - Min: ${min(receipt_values):.2f}, Max: ${max(receipt_values):.2f}, Avg: ${sum(receipt_values)/len(receipt_values):.2f}")
print(f"Output - Min: ${min(output_values):.2f}, Max: ${max(output_values):.2f}, Avg: ${sum(output_values)/len(output_values):.2f}") 