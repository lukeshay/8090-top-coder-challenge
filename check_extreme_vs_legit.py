#!/usr/bin/env python3

# Check the extreme case that should be penalized
days, miles, receipts, expected = 1, 1082, 1809.49, 446.94
product = miles * receipts
print(f'Extreme case: {days}d, {miles}mi, ${receipts:.0f} → ${expected:.0f}')
print(f'Miles × Receipts: {product:.0f}')

# Calculate needed ratio
base = 100.0 * days
mileage = miles * 0.60
receipt_portion = receipts * 0.70
subtotal = base + mileage + receipt_portion
needed_ratio = expected / subtotal
print(f'Needed ratio: {needed_ratio:.3f}')
print()

# Compare with the legitimate cases
legit_cases = [
    (1, 1002, 2320.13, 1475.40),
    (1, 1068, 2011.28, 1421.45)
]

print('Legitimate 1-day high-expense cases:')
for days, miles, receipts, expected in legit_cases:
    product = miles * receipts
    base = 100.0 * days
    mileage = miles * 0.60
    receipt_portion = receipts * 0.70
    subtotal = base + mileage + receipt_portion
    needed_ratio = expected / subtotal
    print(f'{days}d, {miles}mi, ${receipts:.0f} → ${expected:.0f}')
    print(f'Miles × Receipts: {product:.0f}, Needed ratio: {needed_ratio:.3f}')
    print()

print('Key insight: The extreme case needs ratio 0.222 (severe penalty)')
print('Legitimate cases need ratios 0.635-0.662 (light penalties at most)')
print('Maybe use needed ratio as discriminator instead of miles×receipts?') 