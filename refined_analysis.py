#!/usr/bin/env python3

import json
import math
from collections import defaultdict

# Load all cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("REFINED ANALYSIS BASED ON FULL DATASET")
print("=" * 50)

# Let's look at the high error cases more closely
high_receipt_cases = []
long_trip_cases = []
normal_cases = []

for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    receipts_per_day = receipts / days if days > 0 else 0
    
    if receipts_per_day > 300:
        high_receipt_cases.append(case)
    elif days >= 10:
        long_trip_cases.append(case)
    else:
        normal_cases.append(case)

print(f"High receipt cases (>$300/day): {len(high_receipt_cases)}")
print(f"Long trip cases (10+ days): {len(long_trip_cases)}")
print(f"Normal cases: {len(normal_cases)}")

print("\n=== HIGH RECEIPT CASES ANALYSIS ===")
for i, case in enumerate(high_receipt_cases[:10]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    baseline = days * 100 + miles * 0.58
    receipt_effect = output - baseline
    receipts_per_day = receipts / days
    
    print(f"Case: {days} days, {miles} miles, ${receipts:.2f} receipts (${receipts_per_day:.2f}/day)")
    print(f"  Expected: ${output:.2f}, Baseline: ${baseline:.2f}, Receipt effect: ${receipt_effect:.2f}")
    print(f"  Receipt multiplier: {receipt_effect / receipts:.3f}" if receipts > 0 else "  No receipts")
    print()

print("\n=== LONG TRIP CASES ANALYSIS ===")
for i, case in enumerate(long_trip_cases[:10]):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    baseline = days * 100 + miles * 0.58
    trip_effect = output - baseline
    
    print(f"Case: {days} days, {miles} miles, ${receipts:.2f} receipts")
    print(f"  Expected: ${output:.2f}, Baseline: ${baseline:.2f}, Trip effect: ${trip_effect:.2f}")
    print(f"  Per day: ${output/days:.2f}")
    print()

print("\n=== MILEAGE RATE ANALYSIS BY DISTANCE ===")
# Analyze mileage rates by looking at cases with minimal receipts
low_receipt_cases = [case for case in cases if case['input']['total_receipts_amount'] < 50]

distance_groups = defaultdict(list)
for case in low_receipt_cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    # Estimate mileage rate after subtracting per diem
    estimated_per_diem = days * 100
    mileage_contribution = output - estimated_per_diem
    rate_per_mile = mileage_contribution / miles if miles > 0 else 0
    
    if miles < 100:
        distance_groups['0-99'].append(rate_per_mile)
    elif miles < 200:
        distance_groups['100-199'].append(rate_per_mile)
    elif miles < 500:
        distance_groups['200-499'].append(rate_per_mile)
    elif miles < 1000:
        distance_groups['500-999'].append(rate_per_mile)
    else:
        distance_groups['1000+'].append(rate_per_mile)

print("Effective mileage rates by distance (low receipt cases):")
for range_name, rates in distance_groups.items():
    if rates:
        avg_rate = sum(rates) / len(rates)
        print(f"  {range_name} miles: ${avg_rate:.3f}/mile (n={len(rates)})")

print("\n=== RECEIPT EFFECT ANALYSIS ===")
# Group by receipt amounts and see the effect
receipt_groups = defaultdict(list)
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    output = case['expected_output']
    
    baseline = days * 100 + miles * 0.58
    receipt_effect = output - baseline
    receipt_multiplier = receipt_effect / receipts if receipts > 0 else 0
    
    if receipts < 100:
        receipt_groups['$0-99'].append(receipt_multiplier)
    elif receipts < 500:
        receipt_groups['$100-499'].append(receipt_multiplier)
    elif receipts < 1000:
        receipt_groups['$500-999'].append(receipt_multiplier)
    elif receipts < 2000:
        receipt_groups['$1000-1999'].append(receipt_multiplier)
    else:
        receipt_groups['$2000+'].append(receipt_multiplier)

print("Receipt effect multipliers by receipt amount:")
for range_name, multipliers in receipt_groups.items():
    if multipliers:
        avg_multiplier = sum(multipliers) / len(multipliers)
        print(f"  {range_name}: {avg_multiplier:.3f}x receipt amount (n={len(multipliers)})")