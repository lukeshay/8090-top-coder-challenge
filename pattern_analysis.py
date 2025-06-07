#!/usr/bin/env python3

import json
import statistics

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Pattern Analysis: What Makes Some Cases Low vs High Ratio?")
print("=" * 60)

# Focus on high and very_high receipt cases since those show the most variation
high_receipt_cases = []
very_high_receipt_cases = []

for i, case in enumerate(cases):
    input_data = case['input']
    expected = case['expected_output']
    
    days = input_data['trip_duration_days']
    miles = input_data['miles_traveled']
    receipts = input_data['total_receipts_amount']
    
    base = 100 * days + 0.60 * miles + 0.70 * receipts
    ratio = expected / base if base > 0 else 0
    
    receipts_per_day = receipts / days
    miles_per_day = miles / days
    
    data_point = {
        'case': i+1,
        'days': days,
        'miles': miles,
        'receipts': receipts,
        'receipts_per_day': receipts_per_day,
        'miles_per_day': miles_per_day,
        'expected': expected,
        'base': base,
        'ratio': ratio
    }
    
    if 1000 <= receipts < 1500:
        high_receipt_cases.append(data_point)
    elif 1500 <= receipts < 2000:
        very_high_receipt_cases.append(data_point)

# Analyze high receipt cases (1000-1500)
print(f"\nHIGH RECEIPT CASES ($1000-$1500) - {len(high_receipt_cases)} cases")
high_receipt_cases.sort(key=lambda x: x['ratio'])

print("LOWEST ratios:")
for case in high_receipt_cases[:5]:
    print(f"  Case {case['case']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.0f}r ({case['receipts_per_day']:.0f}/day, {case['miles_per_day']:.0f}mi/day) -> ratio {case['ratio']:.3f}")

print("HIGHEST ratios:")
for case in high_receipt_cases[-5:]:
    print(f"  Case {case['case']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.0f}r ({case['receipts_per_day']:.0f}/day, {case['miles_per_day']:.0f}mi/day) -> ratio {case['ratio']:.3f}")

# Analyze very high receipt cases (1500-2000)
print(f"\nVERY HIGH RECEIPT CASES ($1500-$2000) - {len(very_high_receipt_cases)} cases")
very_high_receipt_cases.sort(key=lambda x: x['ratio'])

print("LOWEST ratios:")
for case in very_high_receipt_cases[:5]:
    print(f"  Case {case['case']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.0f}r ({case['receipts_per_day']:.0f}/day, {case['miles_per_day']:.0f}mi/day) -> ratio {case['ratio']:.3f}")

print("HIGHEST ratios:")
for case in very_high_receipt_cases[-5:]:
    print(f"  Case {case['case']}: {case['days']}d, {case['miles']}mi, ${case['receipts']:.0f}r ({case['receipts_per_day']:.0f}/day, {case['miles_per_day']:.0f}mi/day) -> ratio {case['ratio']:.3f}")

# Check if there's a pattern with receipts_per_day vs miles_per_day
print(f"\nPATTERN ANALYSIS:")
print("Looking for correlation between low ratios and receipts_per_day vs miles_per_day...")

low_ratio_cases = [c for c in high_receipt_cases + very_high_receipt_cases if c['ratio'] < 0.4]
high_ratio_cases = [c for c in high_receipt_cases + very_high_receipt_cases if c['ratio'] > 0.8]

print(f"\nLOW RATIO cases (ratio < 0.4) - {len(low_ratio_cases)} cases:")
for case in low_ratio_cases:
    print(f"  Case {case['case']}: {case['days']}d, ${case['receipts_per_day']:.0f}/day, {case['miles_per_day']:.0f}mi/day -> ratio {case['ratio']:.3f}")

print(f"\nHIGH RATIO cases (ratio > 0.8) - {len(high_ratio_cases)} cases:")
for case in high_ratio_cases:
    print(f"  Case {case['case']}: {case['days']}d, ${case['receipts_per_day']:.0f}/day, {case['miles_per_day']:.0f}mi/day -> ratio {case['ratio']:.3f}") 