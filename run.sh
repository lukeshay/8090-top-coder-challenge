#!/bin/bash

# Black Box Challenge - Decision Tree Implementation
# This script takes three parameters and outputs the reimbursement amount
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

# Read the base64 encoded model from the file and use Python to make predictions
python3 -c "
import base64
import pickle
import numpy as np

# Get input parameters
trip_duration_days = float('$1')
miles_traveled = float('$2')
total_receipts_amount = float('$3')

# Base64 encoded model (embedded in script)
model_base64 = '''$(cat model_base64.txt)'''

# Decode the model
model_bytes = base64.b64decode(model_base64)
model_data = pickle.loads(model_bytes)
model = model_data['model']
features = model_data['features']

# Calculate all the features
miles_per_day = miles_traveled / trip_duration_days
receipts_per_day = total_receipts_amount / trip_duration_days
receipt_cents = int(total_receipts_amount * 100) % 100
receipt_ends_49 = int(receipt_cents == 49)
receipt_ends_99 = int(receipt_cents == 99)
is_5_day_trip = int(trip_duration_days == 5)
is_4_6_day_trip = int(4 <= trip_duration_days <= 6)
is_short_trip = int(trip_duration_days <= 3)
is_medium_trip = int(4 <= trip_duration_days <= 7)
is_long_trip = int(trip_duration_days >= 8)
is_efficient = int(180 <= miles_per_day <= 220)
is_highly_efficient = int(miles_per_day > 220)
is_low_efficiency = int(miles_per_day < 50)
miles_0_100 = min(miles_traveled, 100)
miles_100_300 = np.clip(miles_traveled - 100, 0, 200)
miles_300_600 = np.clip(miles_traveled - 300, 0, 300)
miles_600_plus = max(miles_traveled - 600, 0)
low_receipts = int(total_receipts_amount < 50)
very_low_receipts = int(total_receipts_amount < 20)
high_receipts = int(total_receipts_amount > 800)
very_high_receipts = int(total_receipts_amount > 1200)
low_daily_spend = int(receipts_per_day < 75)
medium_daily_spend = int(75 <= receipts_per_day <= 120)
high_daily_spend = int(receipts_per_day > 120)
trip_miles_interaction = trip_duration_days * miles_traveled
trip_receipts_interaction = trip_duration_days * total_receipts_amount
miles_receipts_interaction = miles_traveled * total_receipts_amount
efficiency_receipts = miles_per_day * receipts_per_day
quick_high_mileage = int(trip_duration_days <= 3 and miles_per_day > 150)
long_low_mileage = int(trip_duration_days >= 8 and miles_per_day < 100)
sweet_spot_combo = int(trip_duration_days == 5 and miles_per_day >= 180 and receipts_per_day < 100)
vacation_penalty = int(trip_duration_days >= 8 and receipts_per_day > 150)
log_miles = np.log1p(miles_traveled)
log_receipts = np.log1p(total_receipts_amount)
sqrt_miles = np.sqrt(miles_traveled)
sqrt_receipts = np.sqrt(total_receipts_amount)
miles_squared = miles_traveled ** 2
receipts_squared = total_receipts_amount ** 2
days_squared = trip_duration_days ** 2
receipts_600_800 = int(600 <= total_receipts_amount <= 800)

# Create feature array in the same order as training
X = np.array([[
    trip_duration_days,
    miles_traveled,
    total_receipts_amount,
    miles_per_day,
    receipts_per_day,
    receipt_cents,
    receipt_ends_49,
    receipt_ends_99,
    is_5_day_trip,
    is_4_6_day_trip,
    is_short_trip,
    is_medium_trip,
    is_long_trip,
    is_efficient,
    is_highly_efficient,
    is_low_efficiency,
    miles_0_100,
    miles_100_300,
    miles_300_600,
    miles_600_plus,
    low_receipts,
    very_low_receipts,
    high_receipts,
    very_high_receipts,
    low_daily_spend,
    medium_daily_spend,
    high_daily_spend,
    trip_miles_interaction,
    trip_receipts_interaction,
    miles_receipts_interaction,
    efficiency_receipts,
    quick_high_mileage,
    long_low_mileage,
    sweet_spot_combo,
    vacation_penalty,
    log_miles,
    log_receipts,
    sqrt_miles,
    sqrt_receipts,
    miles_squared,
    receipts_squared,
    days_squared,
    receipts_600_800
]])

# Make prediction
prediction = model.predict(X)[0]

# Round to 2 decimal places
print(f'{prediction:.2f}')
" 