#!/usr/bin/env python3
import subprocess

# Test the new penalty system on high-error cases
cases = [
    (4, 69, 2321.49, 322.00),    # Case 152
    (8, 795, 1645.99, 644.69),  # Case 684  
    (1, 1082, 1809.49, 446.94), # Case 996
    (14, 1056, 2489.69, 1894.16), # Case 242
    (8, 482, 1411.49, 631.81)   # Case 548
]

print('Testing Enhanced Penalty System on High-Error Cases:')
print('=' * 55)

for i, (days, miles, receipts, expected) in enumerate(cases, 1):
    # Run the implementation
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    
    print(f'Case {i}: {days}d, {miles}mi, ${receipts:.2f}')
    print(f'  Expected: ${expected:.2f}')
    print(f'  Got:      ${actual:.2f}')
    print(f'  Error:    ${error:.2f}')
    print() 