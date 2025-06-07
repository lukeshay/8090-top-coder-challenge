import json
import statistics

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print("Error Analysis of Pure Base Ratio Model")
print("=" * 50)

results = []

for i, case in enumerate(cases):
    input_data = case['input']
    expected = case['expected_output']
    
    days = input_data['trip_duration_days']
    miles = input_data['miles_traveled']
    receipts = input_data['total_receipts_amount']
    
    # --- The model being analyzed ---
    base_per_diem = 100.0 * days
    mileage_reimbursement = miles * 0.60
    receipt_reimbursement = receipts * 0.70
    base_total = base_per_diem + mileage_reimbursement + receipt_reimbursement if (base_per_diem + mileage_reimbursement + receipt_reimbursement) > 0 else 1
    
    if days == 1: base_ratio = 0.758
    elif days == 2: base_ratio = 0.807
    elif days == 3: base_ratio = 0.833
    elif days == 4: base_ratio = 0.565
    elif days == 5: base_ratio = 0.828
    elif days == 6: base_ratio = 0.797
    elif days == 7: base_ratio = 0.867
    elif days == 8: base_ratio = 0.746
    elif days == 9: base_ratio = 0.729
    elif days == 10: base_ratio = 0.643
    elif days == 11: base_ratio = 0.723
    elif days == 12: base_ratio = 0.669
    elif days == 13: base_ratio = 0.740
    elif days == 14: base_ratio = 0.649
    else: base_ratio = max(0.6 - (days - 15) * 0.02, 0.4)
    
    actual = round(base_total * base_ratio, 2)
    # --- End of model ---

    error = actual - expected
    
    results.append({
        'case': i+1, 'days': days, 'miles': miles, 'receipts': receipts,
        'expected': expected, 'actual': actual, 'error': error,
        'expected_ratio': expected / base_total if base_total > 0 else 0,
        'actual_ratio': base_ratio
    })

# Sort by absolute error
results.sort(key=lambda x: abs(x['error']), reverse=True)

print("\nTop 20 High Error Cases (Model is Over-paying)")
overpaid = [r for r in results if r['error'] > 0]
for r in overpaid[:20]:
    print(f"  Case {r['case']:4}: Err=${r['error']:7.2f}, Days={r['days']:2}, Rec=${r['receipts']:7.2f}. ExpectedRatio={r['expected_ratio']:.3f}, UsedRatio={r['actual_ratio']:.3f}")

print("\nTop 20 High Error Cases (Model is Under-paying)")
underpaid = [r for r in results if r['error'] < 0]
for r in underpaid[:20]:
    print(f"  Case {r['case']:4}: Err=${r['error']:7.2f}, Days={r['days']:2}, Rec=${r['receipts']:7.2f}. ExpectedRatio={r['expected_ratio']:.3f}, UsedRatio={r['actual_ratio']:.3f}") 