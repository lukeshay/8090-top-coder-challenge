#!/usr/bin/env python3

import json
import statistics

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Comprehensive Receipt Analysis")
print("=" * 50)

# Group cases by receipt levels and analyze ratios
receipt_groups = {
    'low': [],      # <$500
    'med': [],      # $500-$1000
    'high': [],     # $1000-$1500
    'very_high': [], # $1500-$2000
    'extreme': []   # >$2000
}

ratio_data = []

for i, case in enumerate(cases):
    input_data = case['input']
    expected = case['expected_output']
    
    days = input_data['trip_duration_days']
    miles = input_data['miles_traveled']
    receipts = input_data['total_receipts_amount']
    
    base = 100 * days + 0.60 * miles + 0.70 * receipts
    ratio = expected / base if base > 0 else 0
    
    data_point = {
        'case': i+1,
        'days': days,
        'miles': miles,
        'receipts': receipts,
        'expected': expected,
        'base': base,
        'ratio': ratio
    }
    
    ratio_data.append(data_point)
    
    if receipts < 500:
        receipt_groups['low'].append(data_point)
    elif receipts < 1000:
        receipt_groups['med'].append(data_point)
    elif receipts < 1500:
        receipt_groups['high'].append(data_point)
    elif receipts < 2000:
        receipt_groups['very_high'].append(data_point)
    else:
        receipt_groups['extreme'].append(data_point)

# Analyze each group
for group_name, group_data in receipt_groups.items():
    if group_data:
        ratios = [d['ratio'] for d in group_data]
        avg_ratio = statistics.mean(ratios)
        median_ratio = statistics.median(ratios)
        print(f"\n{group_name.upper()} receipt group ({len(group_data)} cases):")
        print(f"  Average ratio: {avg_ratio:.3f}")
        print(f"  Median ratio: {median_ratio:.3f}")
        print(f"  Range: {min(ratios):.3f} - {max(ratios):.3f}")
        
        # Show some examples
        print(f"  Examples:")
        sorted_group = sorted(group_data, key=lambda x: x['ratio'])
        for i in [0, len(sorted_group)//2, -1]:
            if 0 <= i < len(sorted_group):
                d = sorted_group[i]
                print(f"    Case {d['case']}: {d['days']}d, {d['miles']}mi, ${d['receipts']:.0f}r -> ${d['expected']:.0f} (ratio: {d['ratio']:.3f})")

# Analyze specific 8-day cases in different receipt ranges
print(f"\n8-DAY TRIP ANALYSIS:")
eight_day_cases = [d for d in ratio_data if d['days'] == 8]
eight_day_by_receipts = {}

for case in eight_day_cases:
    receipts = case['receipts']
    if receipts < 1000:
        group = "low_med"
    elif receipts < 1500:
        group = "high"
    elif receipts < 2000:
        group = "very_high"
    else:
        group = "extreme"
    
    if group not in eight_day_by_receipts:
        eight_day_by_receipts[group] = []
    eight_day_by_receipts[group].append(case)

for group, cases in eight_day_by_receipts.items():
    ratios = [c['ratio'] for c in cases]
    avg_ratio = statistics.mean(ratios)
    print(f"  {group}: {len(cases)} cases, avg ratio: {avg_ratio:.3f}")
    # Show a few examples
    for case in cases[:3]:
        print(f"    Case {case['case']}: ${case['receipts']:.0f}r -> ${case['expected']:.0f} (ratio: {case['ratio']:.3f})") 