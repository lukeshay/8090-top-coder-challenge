#!/usr/bin/env python3

# Analyze problem cases to understand penalty patterns
problem_cases = [
    (8, 795, 1645.99, 644.69, "Should be heavily penalized"),    # Case 684
    (5, 516, 1878.49, 669.85, "Should be heavily penalized"),   # Case 711 - FIXED
    (8, 482, 1411.49, 631.81, "Should be moderately penalized"), # Case 548
    (5, 781, 2114.27, 1789.85, "Should get near full amount"),  # Case 460 - OVER-PENALIZED
    (5, 1010, 2054.21, 1810.37, "Should get near full amount") # Case 850 - OVER-PENALIZED
]

print('Analysis of Problem Cases - When to Penalize High Receipts:')
print('=' * 65)

for days, miles, receipts, expected, note in problem_cases:
    # Calculate base amounts
    base = 100.0 * days
    mileage = miles * 0.60
    receipt_portion = receipts * 0.70
    subtotal = base + mileage + receipt_portion
    
    # Calculate actual ratio needed
    ratio = expected / subtotal
    
    # Calculate some potential discriminators
    receipts_per_day = receipts / days
    miles_per_day = miles / days
    interaction = miles * receipts
    
    print(f'{days}d, {miles}mi, ${receipts:.0f} → ${expected:.0f} ({note})')
    print(f'  Needed ratio: {ratio:.3f}')
    print(f'  Receipts/day: ${receipts_per_day:.0f}')
    print(f'  Miles/day: {miles_per_day:.0f}')
    print(f'  Miles×Receipts: {interaction:.0f}')
    print()

print('Key Insights:')
print('- Cases 460 & 850: High receipts BUT also high miles → legitimate business trips')
print('- Cases 684, 711, 548: High receipts with low-moderate miles → suspicious')
print('- Maybe penalty should consider miles×receipts ratio, not just receipts')
print('- High miles might justify high receipts (longer distance = more expenses)') 