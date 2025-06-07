#!/usr/bin/env python3
import subprocess

# High-error cases from 18k score evaluation
cases = [
    (8, 892, 1768.53, 1902.37, "8-day UNDER-reimbursed"),        # Case 136
    (5, 516, 1878.49, 669.85, "5-day OVER-reimbursed"),         # Case 711
    (8, 862, 1817.85, 1719.37, "8-day UNDER-reimbursed"),       # Case 41
    (1, 1002, 2320.13, 1475.40, "1-day UNDER-reimbursed"),      # Case 940
    (1, 1068, 2011.28, 1421.45, "1-day UNDER-reimbursed")       # Case 611
]

print('Analysis of 18k Score High-Error Cases:')
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
    print()

print('Key Issues:')
print('1. Cases 136, 41: 8-day trips with good miles getting over-penalized')
print('2. Case 711: 5-day trip getting bonus when it should be penalized')
print('3. Cases 940, 611: 1-day high-expense cases need less penalty')
print('4. 8-day penalty logic needs refinement')
print('5. 5-day bonus logic too generous') 