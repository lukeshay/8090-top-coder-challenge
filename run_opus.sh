#!/bin/bash

# Black Box Challenge - Reimbursement System Implementation
# Based on reverse engineering analysis from employee interviews and data patterns

# Input parameters
trip_duration_days="$1"
miles_traveled="$2"
total_receipts_amount="$3"

# Balanced constants
BASE_PER_DIEM=82
MILEAGE_TIER1_RATE=0.50
MILEAGE_TIER1_LIMIT=100
MILEAGE_TIER2_RATE=0.30

# Calculate base per diem with moderate long trip adjustment
if [ "$trip_duration_days" -le 6 ]; then
    base_per_diem=$(echo "scale=10; $trip_duration_days * $BASE_PER_DIEM" | bc)
else
    # Small adjustment for long trips
    base_per_diem=$(echo "scale=10; $trip_duration_days * $BASE_PER_DIEM * 0.95" | bc)
fi

# Calculate mileage reimbursement with tiered system
if (( $(echo "$miles_traveled <= $MILEAGE_TIER1_LIMIT" | bc -l) )); then
    mileage_reimbursement=$(echo "scale=10; $miles_traveled * $MILEAGE_TIER1_RATE" | bc)
else
    # First 100 miles at full rate, remainder at reduced rate
    tier1_amount=$(echo "scale=10; $MILEAGE_TIER1_LIMIT * $MILEAGE_TIER1_RATE" | bc)
    remaining_miles=$(echo "scale=10; $miles_traveled - $MILEAGE_TIER1_LIMIT" | bc)
    tier2_amount=$(echo "scale=10; $remaining_miles * $MILEAGE_TIER2_RATE" | bc)
    mileage_reimbursement=$(echo "scale=10; $tier1_amount + $tier2_amount" | bc)
fi

# High mileage bonus for legitimate cases
if (( $(echo "$miles_traveled >= 600" | bc -l) )); then
    high_mileage_bonus=$(echo "scale=10; ($miles_traveled - 600) * 0.20" | bc)
    mileage_reimbursement=$(echo "scale=10; $mileage_reimbursement + $high_mileage_bonus" | bc)
fi

# Calculate daily metrics
daily_receipts=$(echo "scale=10; $total_receipts_amount / $trip_duration_days" | bc)
daily_miles=$(echo "scale=10; $miles_traveled / $trip_duration_days" | bc)

# Balanced receipt processing
if (( $(echo "$total_receipts_amount < 25" | bc -l) )); then
    # Small receipts penalty
    receipt_adjustment=$(echo "scale=10; $total_receipts_amount * 0.3" | bc)
elif (( $(echo "$daily_receipts > 400" | bc -l) )); then
    # High daily spending gets reduced rate
    receipt_adjustment=$(echo "scale=10; $total_receipts_amount * 0.4" | bc)
elif (( $(echo "$total_receipts_amount <= 800" | bc -l) )); then
    # Normal receipts - good treatment
    receipt_adjustment=$(echo "scale=10; $total_receipts_amount * 0.75" | bc)
else
    # High receipts - diminishing returns
    base_amount=$(echo "scale=10; 800 * 0.75" | bc)
    excess=$(echo "scale=10; $total_receipts_amount - 800" | bc)
    excess_adjustment=$(echo "scale=10; $excess * 0.40" | bc)
    receipt_adjustment=$(echo "scale=10; $base_amount + $excess_adjustment" | bc)
fi

# Efficiency calculation
efficiency_bonus=0
if (( $(echo "$daily_miles >= 150 && $daily_miles <= 300" | bc -l) )); then
    # Good efficiency range
    efficiency_bonus=$(echo "scale=10; $trip_duration_days * 35" | bc)
elif (( $(echo "$daily_miles > 300 && $daily_miles <= 500" | bc -l) )); then
    # High efficiency
    efficiency_bonus=$(echo "scale=10; $trip_duration_days * 60" | bc)
elif (( $(echo "$daily_miles < 40" | bc -l) )); then
    # Low efficiency penalty
    efficiency_bonus=$(echo "scale=10; $trip_duration_days * -20" | bc)
fi

# 5-day trip bonus
five_day_bonus=0
if [ "$trip_duration_days" -eq 5 ]; then
    five_day_bonus=50
fi

# Calculate total reimbursement
total=$(echo "scale=10; $base_per_diem + $mileage_reimbursement + $receipt_adjustment + $efficiency_bonus + $five_day_bonus" | bc)

# Round to 2 decimal places
result=$(echo "scale=2; ($total + 0.005) / 1" | bc | sed 's/^\./0./')

echo "$result" 