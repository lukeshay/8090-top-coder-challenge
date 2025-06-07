import json
import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error
import pickle
import base64

# Load the data
with open('public_cases.json', 'r') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame([{
    'trip_duration_days': case['input']['trip_duration_days'],
    'miles_traveled': case['input']['miles_traveled'],
    'total_receipts_amount': case['input']['total_receipts_amount'],
    'reimbursement': case['expected_output']
} for case in data])

# Calculate derived features that might be important based on interviews
df['miles_per_day'] = df['miles_traveled'] / df['trip_duration_days']
df['receipts_per_day'] = df['total_receipts_amount'] / df['trip_duration_days']
df['receipt_ends_49'] = (df['total_receipts_amount'] * 100 % 100 == 49).astype(int)
df['receipt_ends_99'] = (df['total_receipts_amount'] * 100 % 100 == 99).astype(int)
df['is_5_day_trip'] = (df['trip_duration_days'] == 5).astype(int)
df['is_efficient'] = ((df['miles_per_day'] >= 180) & (df['miles_per_day'] <= 220)).astype(int)

print("Data Overview:")
print(df.describe())
print("\nFirst few rows:")
print(df.head(10))

# Analyze patterns
print("\n\nPattern Analysis:")
print("\n5-day trip analysis:")
five_day = df[df['trip_duration_days'] == 5]
other_days = df[df['trip_duration_days'] != 5]
print(f"Average reimbursement for 5-day trips: ${five_day['reimbursement'].mean():.2f}")
print(f"Average reimbursement for non-5-day trips: ${other_days['reimbursement'].mean():.2f}")

print("\nEfficiency bonus analysis (180-220 miles/day):")
efficient = df[df['is_efficient'] == 1]
inefficient = df[df['is_efficient'] == 0]
print(f"Average reimbursement for efficient trips: ${efficient['reimbursement'].mean():.2f}")
print(f"Average reimbursement for inefficient trips: ${inefficient['reimbursement'].mean():.2f}")

print("\nPer diem analysis:")
df['base_per_diem'] = df['trip_duration_days'] * 100
df['reimbursement_minus_base'] = df['reimbursement'] - df['base_per_diem']
print(f"Average amount above base per diem: ${df['reimbursement_minus_base'].mean():.2f}")

print("\nReceipt rounding analysis:")
ends_49 = df[df['receipt_ends_49'] == 1]
ends_99 = df[df['receipt_ends_99'] == 1]
normal_receipts = df[(df['receipt_ends_49'] == 0) & (df['receipt_ends_99'] == 0)]
print(f"Receipts ending in .49: {len(ends_49)} cases, avg reimbursement: ${ends_49['reimbursement'].mean():.2f}")
print(f"Receipts ending in .99: {len(ends_99)} cases, avg reimbursement: ${ends_99['reimbursement'].mean():.2f}")
print(f"Other receipts: {len(normal_receipts)} cases, avg reimbursement: ${normal_receipts['reimbursement'].mean():.2f}")

# Train decision tree
print("\n\nTraining Decision Tree...")

# Prepare features for the decision tree
features = [
    'trip_duration_days',
    'miles_traveled', 
    'total_receipts_amount',
    'miles_per_day',
    'receipts_per_day',
    'receipt_ends_49',
    'receipt_ends_99',
    'is_5_day_trip',
    'is_efficient'
]

X = df[features]
y = df['reimbursement']

# Train with max_depth=20 as specified
dt = DecisionTreeRegressor(max_depth=20, random_state=42)
dt.fit(X, y)

# Check accuracy
y_pred = dt.predict(X)
mae = mean_absolute_error(y, y_pred)
print(f"Mean Absolute Error on training data: ${mae:.2f}")

# Check exact matches (within $0.01)
exact_matches = np.sum(np.abs(y - y_pred) < 0.01)
print(f"Exact matches (within $0.01): {exact_matches}/{len(y)} ({exact_matches/len(y)*100:.1f}%)")

# Save the model
with open('decision_tree_model.pkl', 'wb') as f:
    pickle.dump({
        'model': dt,
        'features': features
    }, f)

print("\nModel saved to decision_tree_model.pkl")

# Create base64 encoded version for embedding
with open('decision_tree_model.pkl', 'rb') as f:
    model_bytes = f.read()
    model_base64 = base64.b64encode(model_bytes).decode('ascii')

print(f"\nBase64 encoded model length: {len(model_base64)} characters")

# Save base64 version to file
with open('model_base64.txt', 'w') as f:
    f.write(model_base64)

print("Base64 encoded model saved to model_base64.txt") 