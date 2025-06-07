#!/usr/bin/env python3
import subprocess

# Latest problematic cases
cases = [
    (5, 320, 1584.55, 1584.73, "Over-penalized"),   # Case 540
    (1, 1082, 1809.49, 446.94, "Under-penalized"),  # Case 996
    (6, 475, 1800.71, 1671.23, "Over-penalized"),   # Case 210
    (7, 381, 2106.96, 1705.27, "Over-penalized"),   # Case 723
    (4, 217, 1506.46, 1455.37, "Over-penalized")    # Case 465
]

print('Testing Refined Smart Penalty System:')
print('=' * 40)

total_error = 0
for days, miles, receipts, expected, issue in cases:
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    total_error += error
    
    print(f'{days}d, {miles}mi, ${receipts:.0f} → ${expected:.0f} ({issue})')
    print(f'  Expected: ${expected:.2f}, Got: ${actual:.2f}, Error: ${error:.2f}')
    print()

print(f'Average error: ${total_error/len(cases):.2f}') 