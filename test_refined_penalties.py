#!/usr/bin/env python3
import subprocess

# Latest high-error cases
cases = [
    (8, 795, 1645.99, 644.69),    # Case 684
    (5, 516, 1878.49, 669.85),   # Case 711
    (8, 482, 1411.49, 631.81),   # Case 548
    (5, 781, 2114.27, 1789.85),  # Case 460
    (5, 1010, 2054.21, 1810.37)  # Case 850
]

print('Testing Refined Penalties on Latest High-Error Cases:')
print('=' * 55)

total_error = 0
for i, (days, miles, receipts, expected) in enumerate(cases, 1):
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    total_error += error
    
    print(f'Case {i}: {days}d, {miles}mi, ${receipts:.2f}')
    print(f'  Expected: ${expected:.2f}, Got: ${actual:.2f}, Error: ${error:.2f}')

print(f'\nAverage error: ${total_error/len(cases):.2f}') 