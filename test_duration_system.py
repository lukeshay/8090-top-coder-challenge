#!/usr/bin/env python3
import subprocess

# Original high-error cases (were under-penalized) 
original_cases = [
    (4, 69, 2321.49, 322.00),    # Case 152
    (8, 795, 1645.99, 644.69),  # Case 684  
    (1, 1082, 1809.49, 446.94), # Case 996
    (14, 1056, 2489.69, 1894.16), # Case 242
    (8, 482, 1411.49, 631.81)   # Case 548
]

# New high-error cases (were over-penalized)
new_cases = [
    (13, 1140, 1607.8, 2214.64),   # Case 590
    (14, 1122, 1766.25, 2239.35), # Case 385  
    (7, 1006, 1181.33, 2279.82),  # Case 149
    (11, 1106, 2250.54, 2050.62), # Case 584
    (7, 1010, 1514.03, 2063.98)   # Case 135
]

print('Testing Duration-Based System on Both Problem Sets:')
print('=' * 55)

print('\nOriginal High-Error Cases (should be penalized more):')
print('-' * 50)
total_error_orig = 0
for i, (days, miles, receipts, expected) in enumerate(original_cases, 1):
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    total_error_orig += error
    
    print(f'Case {i}: {days}d, {miles}mi, ${receipts:.2f}')
    print(f'  Expected: ${expected:.2f}, Got: ${actual:.2f}, Error: ${error:.2f}')

print(f'\nAverage error (original): ${total_error_orig/len(original_cases):.2f}')

print('\nNew High-Error Cases (should be penalized less):')
print('-' * 50)
total_error_new = 0
for i, (days, miles, receipts, expected) in enumerate(new_cases, 1):
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    total_error_new += error
    
    print(f'Case {i}: {days}d, {miles}mi, ${receipts:.2f}')
    print(f'  Expected: ${expected:.2f}, Got: ${actual:.2f}, Error: ${error:.2f}')

print(f'\nAverage error (new): ${total_error_new/len(new_cases):.2f}')
print(f'Overall average error: ${(total_error_orig + total_error_new)/(len(original_cases) + len(new_cases)):.2f}') 