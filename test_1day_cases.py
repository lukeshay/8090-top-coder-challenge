#!/usr/bin/env python3
import subprocess

# Test cases: legitimate 1-day trips vs extreme case
cases = [
    (1, 1058, 1601.04, 1465.90, "Legitimate high-mileage 1-day"),  # Case 713
    (1, 1041, 1630.25, 1466.95, "Legitimate high-mileage 1-day"),  # Case 921
    (1, 809, 1734.56, 1447.25, "Legitimate high-mileage 1-day"),   # Case 749
    (1, 1082, 1809.49, 446.94, "Extreme case - should be penalized"), # Case 996
]

print('Testing Fine-Tuned 1-Day Case Handling:')
print('=' * 45)

total_error = 0
for days, miles, receipts, expected, description in cases:
    result = subprocess.run(['./run.sh', str(days), str(miles), str(receipts)], 
                          capture_output=True, text=True)
    actual = float(result.stdout.strip())
    error = abs(actual - expected)
    total_error += error
    
    # Calculate what the base ratio would be
    base = 100.0 * days
    mileage = miles * 0.60
    receipt_portion = receipts * 0.70
    subtotal = base + mileage + receipt_portion
    needed_ratio = expected / subtotal
    
    print(f'{days}d, {miles}mi, ${receipts:.0f} ({description})')
    print(f'  Expected: ${expected:.2f} (ratio {needed_ratio:.3f})')
    print(f'  Got: ${actual:.2f}, Error: ${error:.2f}')
    print()

print(f'Average error: ${total_error/len(cases):.2f}') 