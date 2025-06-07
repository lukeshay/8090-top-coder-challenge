#!/usr/bin/env python3

# Analysis of high-error cases from latest evaluation
cases = [
    (4, 69, 2321.49, 322.00),    # Case 152
    (8, 795, 1645.99, 644.69),  # Case 684  
    (1, 1082, 1809.49, 446.94), # Case 996
    (14, 1056, 2489.69, 1894.16), # Case 242
    (8, 482, 1411.49, 631.81)   # Case 548
]

print('Analysis of High-Error Cases:')
print('=' * 50)
for i, (days, miles, receipts, expected) in enumerate(cases, 1):
    # Current formula
    base = 100.0 * days
    mileage = miles * 0.60
    receipt_portion = receipts * 0.70
    subtotal = base + mileage + receipt_portion
    
    # Check complexity
    is_complex = (miles > 300 or receipts > 400 or (miles > 200 and receipts > 200))
    current_result = subtotal * 0.75 if is_complex else subtotal
    
    # What would the ratio need to be?
    needed_ratio = expected / subtotal if subtotal > 0 else 0
    
    print(f'Case {i}: {days}d, {miles}mi, ${receipts:.2f}')
    print(f'  Base: ${base:.2f}, Miles: ${mileage:.2f}, Receipts: ${receipt_portion:.2f}')
    print(f'  Subtotal: ${subtotal:.2f}')
    print(f'  Complex: {is_complex}, Current: ${current_result:.2f}')
    print(f'  Expected: ${expected:.2f}, Needed ratio: {needed_ratio:.3f}')
    print(f'  Miles×Receipts: {miles * receipts:.0f}')
    print()

print('Key Observations:')
print('- All cases have very high receipts (>$1400)')
print('- All are marked as complex')
print('- Current 0.75 penalty is way too lenient')
print('- Needed ratios are much lower (0.1-0.4 range)')
print('- These cases need severe penalties based on receipt amounts') 