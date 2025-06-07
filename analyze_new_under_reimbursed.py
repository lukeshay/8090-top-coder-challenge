#!/usr/bin/env python3
import subprocess

# New under-reimbursed cases 
cases = [
    (7, 623, 1691.39, 1800.86, "7-day UNDER-reimbursed"),     # Case 271
    (4, 84, 2243.12, 1392.10, "4-day UNDER-reimbursed"),     # Case 893
    (4, 87, 2463.92, 1413.52, "4-day UNDER-reimbursed"),     # Case 175
    (6, 384, 1656.04, 1682.33, "6-day UNDER-reimbursed"),    # Case 794
    (3, 29, 1632.85, 1269.10, "3-day UNDER-reimbursed")      # Case 618
]

print('Analysis of New Under-Reimbursed Cases:')
print('=' * 45)

for days, miles, receipts, expected, description in cases:
    # Calculate what we currently produce
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    
    # Calculate base metrics
    base = 100.0 * days
    mileage = miles * 0.60
    receipt_portion = receipts * 0.70
    subtotal = base + mileage + receipt_portion
    needed_ratio = expected / subtotal
    actual_ratio = actual / subtotal
    
    miles_per_day = miles / days
    receipts_per_day = receipts / days
    
    print(f'{days}d, {miles}mi, ${receipts:.0f} ({description})')
    print(f'  Expected: ${expected:.0f} (ratio {needed_ratio:.3f})')
    print(f'  Got: ${actual:.0f} (ratio {actual_ratio:.3f}), Error: ${error:.0f}')
    print(f'  Miles/day: {miles_per_day:.0f}, Receipts/day: ${receipts_per_day:.0f}')
    
    # Determine which penalty is being applied
    if receipts_per_day > 500 and miles_per_day < 30:
        penalty_type = "Severe penalty (0.20) - Very high receipts + very low miles"
    elif days == 1 and miles > 1000 and receipts > 1700:
        penalty_type = "Severe penalty (0.30) - Extreme 1-day case"
    elif receipts_per_day > 200 and miles_per_day < 100 and days <= 8:
        penalty_type = "Moderate penalty (0.40) - High receipts + low miles on short trips"
    else:
        penalty_type = "Other penalty"
    
    print(f'  Penalty applied: {penalty_type}')
    print()

print('Key Issue: Many legitimate cases are getting severe penalties')
print('Need to be more selective about when to apply penalties') 