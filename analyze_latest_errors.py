#!/usr/bin/env python3
import subprocess

# Latest high-error cases from evaluation
cases = [
    (1, 1002, 2320.13, 1475.40, "1-day extreme receipts - under-reimbursed"),  # Case 940
    (10, 793, 1422.29, 2007.62, "10-day long trip - under-reimbursed"),       # Case 556
    (3, 133, 1728.5, 1373.40, "3-day low miles high receipts - under-reimbursed"), # Case 527
    (1, 1068, 2011.28, 1421.45, "1-day extreme receipts - under-reimbursed"), # Case 611
    (12, 1189, 1453.16, 2162.13, "12-day long trip - under-reimbursed")       # Case 695
]

print('Analysis of Latest High-Error Cases:')
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
    
    # Determine what penalty was applied
    duration_ratios = {1: 0.756, 3: 0.785, 10: 0.666, 12: 0.646}
    base_ratio = duration_ratios.get(days, 0.70)
    penalty_applied = actual_ratio / base_ratio if base_ratio > 0 else 1.0
    
    print(f'  Base duration ratio: {base_ratio:.3f}, Penalty applied: {penalty_applied:.3f}')
    print()

print('Key Observations:')
print('- Cases 940, 611: 1-day trips with >$2000 receipts need higher ratios (~0.73-0.82), not penalties')
print('- Case 527: 3-day low-miles case needs ratio 0.88, much higher than base 0.785')
print('- Cases 556, 695: Long trips need higher ratios than base duration ratios suggest')
print('- Some high-receipt cases are actually legitimate and should get bonuses, not penalties') 