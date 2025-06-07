#!/usr/bin/env python3

import json
import statistics

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Analyzing patterns in reimbursement system...")
print("=" * 50)

# Analyze first 200 cases to understand base patterns
ratios_by_days = {}
errors_high_receipt = []

for i, case in enumerate(cases[:200]):
    input_data = case['input']
    expected = case['expected_output']
    
    days = input_data['trip_duration_days']
    miles = input_data['miles_traveled']
    receipts = input_data['total_receipts_amount']
    
    # Simple base formula
    base = 100 * days + 0.60 * miles + 0.70 * receipts
    ratio = expected / base if base > 0 else 0
    
    if days not in ratios_by_days:
        ratios_by_days[days] = []
    ratios_by_days[days].append(ratio)
    
    # Check high receipt cases
    if receipts > 1000:
        errors_high_receipt.append({
            'case': i+1,
            'days': days,
            'miles': miles,
            'receipts': receipts,
            'expected': expected,
            'base': base,
            'ratio': ratio
        })

print("\nAverage ratios by trip duration:")
for days in sorted(ratios_by_days.keys()):
    avg_ratio = statistics.mean(ratios_by_days[days])
    print(f"{days} days: {avg_ratio:.3f} (n={len(ratios_by_days[days])})")

print(f"\nHigh receipt cases (>${1000}):")
for case in errors_high_receipt[:10]:
    print(f"Case {case['case']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.2f}r -> ${case['expected']:.2f} (ratio: {case['ratio']:.3f})")

# Test our high-error cases specifically
print(f"\nAnalyzing the 5 highest error cases:")
target_cases = [684-1, 247-1, 462-1, 264-1, 996-1]
for i in target_cases:
    case = cases[i]
    input_data = case['input']
    expected = case['expected_output']
    
    days = input_data['trip_duration_days']
    miles = input_data['miles_traveled']
    receipts = input_data['total_receipts_amount']
    
    base = 100 * days + 0.60 * miles + 0.70 * receipts
    ratio = expected / base if base > 0 else 0
    
    print(f"Case {i+1}: {days}d, {miles}mi, ${receipts:.2f}r -> ${expected:.2f} (base: ${base:.2f}, ratio: {ratio:.3f})") 