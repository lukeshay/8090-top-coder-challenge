#!/usr/bin/env python3
import subprocess

# New 5-day high-error cases
cases = [
    (5, 789, 1853.31, 1792.88, "5-day UNDER-reimbursed"),    # Case 369
    (5, 781, 2114.27, 1789.85, "5-day UNDER-reimbursed"),    # Case 460
    (5, 1010, 2054.21, 1810.37, "5-day UNDER-reimbursed"),   # Case 850
    (5, 1014, 1853.57, 1749.31, "5-day UNDER-reimbursed"),   # Case 378
    (5, 644, 2383.17, 1785.53, "5-day UNDER-reimbursed")     # Case 944
]

print('Analysis of 5-Day Trip Issues:')
print('=' * 35)

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
    
    # Determine which penalty is likely being applied
    if receipts_per_day > 350 and miles_per_day > 100:
        penalty_type = "Case 711 fix penalty (0.40) - problematic for legitimate cases"
    elif receipts_per_day > 300 and miles_per_day < 50:
        penalty_type = "High receipts + low miles penalty (0.60)"
    elif receipts_per_day > 500 and miles_per_day < 40:
        penalty_type = "Stationary business bonus (1.05)"
    else:
        penalty_type = "Base 5-day ratio (0.790) or light penalty (0.90)"
    
    print(f'  Likely penalty: {penalty_type}')
    print()

print('Key Issue: Case 711 fix penalty is too broad and affecting legitimate 5-day trips')
print('All these cases have high miles AND high receipts - they should get base ratio or bonuses')
print('Need to make the 5-day penalty more specific to Case 711 pattern') 