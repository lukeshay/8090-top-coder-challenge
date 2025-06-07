#!/usr/bin/env python3

import json

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

# Extract 1-day trips for detailed analysis
one_day_cases = [case for case in cases if case['input']['trip_duration_days'] == 1]

print("Analyzing specific problematic cases:")

# Look at the specific high-error cases
problem_cases = [
    (37, 1397.17, 1092.94),   # Case 29
    (451, 555.49, 162.18),    # Case 14
    (123, 2076.65, 1171.68),  # Case 25
    (989, 2196.84, 1439.17),  # Case 28
    (822, 2170.53, 1374.91),  # Case 26
]

for miles, receipts, expected in problem_cases:
    print(f"\nMiles: {miles}, Receipts: ${receipts:.2f}, Expected: ${expected:.2f}")
    
    # Calculate ratios
    receipt_ratio = expected / receipts if receipts > 0 else 0
    per_mile = expected / miles if miles > 0 else 0
    
    print(f"  Receipt ratio: {receipt_ratio:.3f}")
    print(f"  Per mile: ${per_mile:.3f}")
    
    # What if there's a maximum cap?
    if expected < receipts * 0.6:  # Less than 60% of receipts
        print(f"  Possible cap or penalty - getting only {receipt_ratio:.1%} of receipts")

print("\n" + "="*60)

# Look for patterns in low reimbursement vs input amounts
print("Looking for cases where reimbursement << inputs:")

suspicious_cases = []
for case in one_day_cases:
    inp = case['input']
    expected = case['expected_output']
    
    total_input = inp['miles_traveled'] * 0.5 + inp['total_receipts_amount']  # rough input estimate
    if expected < total_input * 0.4:  # Reimbursement is less than 40% of rough inputs
        suspicious_cases.append(case)

print(f"Found {len(suspicious_cases)} suspicious cases:")
for case in suspicious_cases:
    inp = case['input']
    expected = case['expected_output']
    
    total_rough = inp['miles_traveled'] * 0.5 + inp['total_receipts_amount']
    ratio = expected / total_rough
    
    print(f"  {inp['miles_traveled']:3.0f} miles, ${inp['total_receipts_amount']:6.2f} receipts → ${expected:7.2f} ({ratio:.1%} of rough inputs)")

print("\n" + "="*60)

# Look for very high receipt cases to understand the penalty
print("High receipt cases (>$1000) analysis:")
high_receipt_cases = [case for case in one_day_cases if case['input']['total_receipts_amount'] > 1000]

for case in high_receipt_cases:
    inp = case['input']
    expected = case['expected_output']
    
    # What would different models predict?
    simple_model = 90 + inp['miles_traveled'] * 0.5 + inp['total_receipts_amount'] * 0.5
    capped_model = min(simple_model, 1200)  # Test if there's a cap
    receipt_penalty_model = 90 + inp['miles_traveled'] * 0.5 + min(inp['total_receipts_amount'], 400) + (inp['total_receipts_amount'] - 400) * 0.2 if inp['total_receipts_amount'] > 400 else 90 + inp['miles_traveled'] * 0.5 + inp['total_receipts_amount']
    
    print(f"\n  {inp['miles_traveled']:3.0f} miles, ${inp['total_receipts_amount']:7.2f} receipts → ${expected:7.2f}")
    print(f"    Simple model: ${simple_model:.2f}")
    print(f"    Capped model: ${capped_model:.2f}")
    print(f"    Penalty model: ${receipt_penalty_model:.2f}")
    print(f"    Closest model: ", end="")
    
    errors = [
        abs(expected - simple_model),
        abs(expected - capped_model), 
        abs(expected - receipt_penalty_model)
    ]
    best = min(errors)
    if best == errors[0]:
        print("Simple")
    elif best == errors[1]:
        print("Capped")
    else:
        print("Penalty")

# Check if there's a relationship between miles and receipts that creates penalties
print("\n" + "="*60)
print("Looking for interaction effects between miles and receipts:")

for case in suspicious_cases[:5]:
    inp = case['input']
    expected = case['expected_output']
    
    # Test if high miles + high receipts = penalty
    miles_receipts_product = inp['miles_traveled'] * inp['total_receipts_amount']
    print(f"  {inp['miles_traveled']:3.0f} miles × ${inp['total_receipts_amount']:6.2f} receipts = {miles_receipts_product:8.0f}")
    print(f"    Expected: ${expected:7.2f}")
    
    if miles_receipts_product > 200000:  # Arbitrary threshold
        print(f"    High product - possible penalty trigger") 