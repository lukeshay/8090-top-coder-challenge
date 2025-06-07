#!/usr/bin/env python3

# New high-error cases
cases = [
    (5, 320, 1584.55, 1584.73, "Over-penalized"),   # Case 540
    (1, 1082, 1809.49, 446.94, "Under-penalized"),  # Case 996
    (6, 475, 1800.71, 1671.23, "Over-penalized"),   # Case 210
    (7, 381, 2106.96, 1705.27, "Over-penalized"),   # Case 723
    (4, 217, 1506.46, 1455.37, "Over-penalized")    # Case 465
]

print('Analysis of New High-Error Cases:')
print('=' * 40)

for days, miles, receipts, expected, issue in cases:
    # Calculate metrics
    base = 100.0 * days
    mileage = miles * 0.60
    receipt_portion = receipts * 0.70
    subtotal = base + mileage + receipt_portion
    ratio = expected / subtotal
    
    miles_per_day = miles / days
    receipts_per_day = receipts / days
    
    print(f'{days}d, {miles}mi, ${receipts:.0f} → ${expected:.0f} ({issue})')
    print(f'  Needed ratio: {ratio:.3f}')
    print(f'  Miles/day: {miles_per_day:.0f}, Receipts/day: ${receipts_per_day:.0f}')
    
    # What would my current logic do?
    if receipts > 1400:
        if miles_per_day >= 150 and receipts_per_day >= 400:
            penalty = 1.0
        elif miles_per_day >= 120 and receipts_per_day >= 350:
            penalty = 0.85
        elif miles_per_day < 100 and receipts_per_day > 300:
            penalty = 0.35
        elif miles_per_day < 120 and receipts_per_day > 350:
            penalty = 0.50
        else:
            penalty = 0.65
    else:
        penalty = 1.0
    
    print(f'  My penalty: {penalty:.2f}')
    print()

print('Key Issues:')
print('- Cases 540, 210, 723, 465: Need higher ratios (0.8-0.9) but getting heavy penalties')
print('- These have moderate miles but high receipts - maybe legitimate for certain trip types')
print('- Case 996: 1-day extreme case needs severe penalty but getting none')
print('- Need to distinguish between trip types that justify high receipts') 