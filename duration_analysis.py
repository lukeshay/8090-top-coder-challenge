#!/usr/bin/env python3
import json

# Load all test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print('Analysis of Penalty/Bonus Structure by Trip Duration:')
print('=' * 55)

# Group by duration and analyze patterns
by_duration = {}
for case in cases:
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    expected = case['expected_output']
    
    # Calculate theoretical subtotal
    base = 100.0 * days
    mileage = miles * 0.60
    receipt_portion = receipts * 0.70
    subtotal = base + mileage + receipt_portion
    
    # Calculate actual ratio
    ratio = expected / subtotal if subtotal > 0 else 0
    
    if days not in by_duration:
        by_duration[days] = []
    
    by_duration[days].append({
        'miles': miles,
        'receipts': receipts,
        'expected': expected,
        'subtotal': subtotal,
        'ratio': ratio,
        'interaction': miles * receipts
    })

# Analyze each duration
for days in sorted(by_duration.keys()):
    data = by_duration[days]
    
    # Calculate statistics
    ratios = [d['ratio'] for d in data]
    avg_ratio = sum(ratios) / len(ratios)
    
    # Find patterns
    bonuses = [d for d in data if d['ratio'] > 1.0]
    severe_penalties = [d for d in data if d['ratio'] < 0.5]
    
    print(f'{days}-day trips ({len(data)} cases):')
    print(f'  Average ratio: {avg_ratio:.3f}')
    print(f'  Bonuses (>1.0): {len(bonuses)} cases')
    print(f'  Severe penalties (<0.5): {len(severe_penalties)} cases')
    
    if len(data) >= 10:  # Only analyze if enough samples
        # Look at extreme cases
        highest_ratio = max(data, key=lambda x: x['ratio'])
        lowest_ratio = min(data, key=lambda x: x['ratio'])
        
        print(f'  Highest ratio: {highest_ratio["ratio"]:.3f} ({highest_ratio["miles"]}mi, ${highest_ratio["receipts"]:.0f})')
        print(f'  Lowest ratio: {lowest_ratio["ratio"]:.3f} ({lowest_ratio["miles"]}mi, ${lowest_ratio["receipts"]:.0f})')
    
    print()

print('Key Insights:')
print('- Longer trips might have different penalty/bonus structures')
print('- Need to balance high-receipt penalties with legitimate long-trip bonuses')
print('- Duration appears to be a critical factor in the calculation') 