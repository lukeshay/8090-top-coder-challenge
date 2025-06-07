#!/bin/bash

# Black Box Challenge - Sonnet Implementation
# Adding multiple calculation paths based on spending patterns

# Input parameters
trip_duration=$1
miles_traveled=$2
total_receipts=$3

# Base per diem - but with long trip penalties
if [ "$trip_duration" -le 7 ]; then
    base_per_diem=$(echo "scale=2; $trip_duration * 95" | bc)
else
    # Penalty for 8+ day trips (vacation penalty from interviews)
    base_per_diem=$(echo "scale=2; $trip_duration * 70" | bc)
fi

# Mileage calculation with diminishing returns for high mileage
if [ $(echo "$miles_traveled <= 200" | bc) -eq 1 ]; then
    mileage_reimbursement=$(echo "scale=2; $miles_traveled * 0.6" | bc)
else
    # First 200 miles at full rate, remainder at much lower rate
    first_tier=$(echo "scale=2; 200 * 0.6" | bc)
    remaining_miles=$(echo "scale=2; $miles_traveled - 200" | bc)
    second_tier=$(echo "scale=2; $remaining_miles * 0.2" | bc)
    mileage_reimbursement=$(echo "scale=2; $first_tier + $second_tier" | bc)
fi

# Multiple calculation paths based on spending patterns
spending_per_day=$(echo "scale=2; $total_receipts / $trip_duration" | bc)

# Special handling for 1-day trips (more generous but with extreme spending penalty)
if [ "$trip_duration" -eq 1 ]; then
    if [ $(echo "$spending_per_day > 1500" | bc) -eq 1 ]; then
        # Extreme spending 1-day trips - severe penalty
        receipt_adjustment=$(echo "scale=2; $total_receipts * 0.2" | bc)
    elif [ $(echo "$spending_per_day > 1000" | bc) -eq 1 ]; then
        # Very high spending 1-day trips - cap but still generous
        receipt_adjustment=$(echo "scale=2; $total_receipts * 0.8" | bc)
    else
        # Regular 1-day trips - more generous treatment
        receipt_adjustment=$(echo "scale=2; $total_receipts * 0.9" | bc)
    fi
# Special handling for 2-day trips (generally more generous)
elif [ "$trip_duration" -eq 2 ]; then
    if [ $(echo "$spending_per_day > 1500" | bc) -eq 1 ]; then
        # Very high spending 2-day trips - still generous
        receipt_adjustment=$(echo "scale=2; $total_receipts * 0.7" | bc)
    elif [ $(echo "$spending_per_day > 1000" | bc) -eq 1 ]; then
        # High spending 2-day trips - moderate treatment
        receipt_adjustment=$(echo "scale=2; $total_receipts * 0.6" | bc)
    elif [ $(echo "$miles_traveled > 800" | bc) -eq 1 ]; then
        # 2-day high-mileage trips get generous treatment
        receipt_adjustment=$(echo "scale=2; $total_receipts * 0.8" | bc)
    else
        # Regular 2-day trips - generous treatment
        receipt_adjustment=$(echo "scale=2; $total_receipts * 0.75" | bc)
    fi
# Special handling for 3-day trips with high spending
elif [ "$trip_duration" -eq 3 ] && [ $(echo "$spending_per_day > 500" | bc) -eq 1 ]; then
    # 3-day high-spending trips get moderate treatment
    receipt_adjustment=$(echo "scale=2; $total_receipts * 0.6" | bc)
else
    # Multi-day trips - use existing logic
    # Determine optimal spending limit based on trip length (from Kevin's insights)
    if [ "$trip_duration" -le 3 ]; then
        optimal_limit=75
    elif [ "$trip_duration" -le 6 ]; then
        optimal_limit=120
    else
        optimal_limit=90
    fi

    # Choose calculation path based on spending behavior
    if [ $(echo "$spending_per_day > 400" | bc) -eq 1 ]; then
        # Extreme overspending path - minimal receipt reimbursement
        receipt_adjustment=$(echo "scale=2; $trip_duration * 50" | bc)
    elif [ $(echo "$spending_per_day <= $optimal_limit" | bc) -eq 1 ]; then
        # Good spending behavior - full reimbursement
        receipt_adjustment=$total_receipts
    elif [ $(echo "$spending_per_day <= 200" | bc) -eq 1 ]; then
        # Moderate overspending - partial penalty
        good_amount=$(echo "scale=2; $trip_duration * $optimal_limit" | bc)
        excess=$(echo "scale=2; $total_receipts - $good_amount" | bc)
        penalty=$(echo "scale=2; $excess * 0.5" | bc)
        receipt_adjustment=$(echo "scale=2; $good_amount + $penalty" | bc)
    else
        # Severe overspending - major penalty
        good_amount=$(echo "scale=2; $trip_duration * $optimal_limit" | bc)
        moderate_amount=$(echo "scale=2; $trip_duration * 200" | bc)
        moderate_excess=$(echo "scale=2; $moderate_amount - $good_amount" | bc)
        severe_excess=$(echo "scale=2; $total_receipts - $moderate_amount" | bc)
        
        if [ $(echo "$severe_excess > 0" | bc) -eq 1 ]; then
            receipt_adjustment=$(echo "scale=2; $good_amount + $moderate_excess * 0.5 + $severe_excess * 0.1" | bc)
        else
            receipt_adjustment=$(echo "scale=2; $good_amount + ($total_receipts - $good_amount) * 0.5" | bc)
        fi
    fi

    # Special penalty for 8+ day trips with high spending (vacation penalty)
    if [ "$trip_duration" -ge 8 ] && [ $(echo "$spending_per_day > 150" | bc) -eq 1 ]; then
        # Apply additional vacation penalty - cap receipts severely
        vacation_cap=$(echo "scale=2; $trip_duration * 30" | bc)
        if [ $(echo "$receipt_adjustment > $vacation_cap" | bc) -eq 1 ]; then
            receipt_adjustment=$vacation_cap
        fi
    fi
fi

# Combine all components
final_amount=$(echo "scale=2; $base_per_diem + $mileage_reimbursement + $receipt_adjustment" | bc)

echo $final_amount 