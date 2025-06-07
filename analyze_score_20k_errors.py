#!/usr/bin/env python3
import subprocess

# High-error cases from the 20k score evaluation
cases = [
    (4, 69, 2321.49, 322.00, "Short trip extreme receipts - OVER-reimbursed"),     # Case 152
    (1, 1082, 1809.49, 446.94, "1-day extreme case - OVER-reimbursed"),           # Case 996
    (13, 1034, 2477.98, 1842.24, "13-day trip - OVER-reimbursed"),               # Case 318
    (13, 1186, 2462.26, 1906.35, "13-day trip - OVER-reimbursed"),               # Case 793
    (8, 795, 1645.99, 644.69, "8-day high receipts - OVER-reimbursed")            # Case 684
]

print('Analysis of High-Error Cases (Score ~20k):')
print('=' * 50)

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
    print()

print('Key Issues:')
print('1. Case 152: Short trip with extreme receipts needs SEVERE penalty (0.15 ratio)')
print('2. Case 996: Original extreme case needs penalty (0.22 ratio)')  
print('3. Cases 318, 793: 13-day trips getting too much bonus')
print('4. Case 684: 8-day case needs moderate penalty (0.27 ratio)')
print('5. System is now over-reimbursing many cases that need penalties') 