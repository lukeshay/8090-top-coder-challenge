#!/bin/bash

# Try to reverse engineer the exact formula by focusing on patterns

days=$1
miles=$2
receipts=$3

# From analysis: seems like base per day + scaled mileage + receipt factors
# But the scaling factors change based on ranges

# Base amount seems to be around 100 per day for most cases
base_amount=$(echo "scale=2; $days * 100" | bc)

# Mileage calculation with diminishing returns
if [ $(echo "$miles <= 50" | bc) -eq 1 ]; then
    # Very low mileage gets a bonus to reach minimum levels
    mileage_amount=$(echo "scale=2; 50 * 2.0 + ($miles - 50) * 8.0" | bc)
elif [ $(echo "$miles <= 150" | bc) -eq 1 ]; then
    # Standard mileage rate
    mileage_amount=$(echo "scale=2; $miles * 2.0" | bc)
elif [ $(echo "$miles <= 400" | bc) -eq 1 ]; then
    # Medium mileage - slightly lower rate
    mileage_amount=$(echo "scale=2; 150 * 2.0 + ($miles - 150) * 1.6" | bc)
elif [ $(echo "$miles <= 800" | bc) -eq 1 ]; then
    # High mileage - further reduced rate
    base_300=$(echo "scale=2; 150 * 2.0 + 250 * 1.6" | bc)
    mileage_amount=$(echo "scale=2; $base_300 + ($miles - 400) * 1.2" | bc)
else
    # Very high mileage - lowest rate
    base_800=$(echo "scale=2; 150 * 2.0 + 250 * 1.6 + 400 * 1.2" | bc)
    mileage_amount=$(echo "scale=2; $base_800 + ($miles - 800) * 0.6" | bc)
fi

# Receipt processing - seems to cap at certain levels
receipt_amount=0
if [ $(echo "$receipts <= 100" | bc) -eq 1 ]; then
    receipt_amount=$(echo "scale=2; $receipts * 0.5" | bc)
elif [ $(echo "$receipts <= 500" | bc) -eq 1 ]; then
    receipt_amount=$(echo "scale=2; 100 * 0.5 + ($receipts - 100) * 0.4" | bc)
elif [ $(echo "$receipts <= 1500" | bc) -eq 1 ]; then
    receipt_amount=$(echo "scale=2; 50 + 400 * 0.4 + ($receipts - 500) * 0.3" | bc)
else
    # Very high receipts get heavily diminished
    receipt_amount=$(echo "scale=2; 50 + 160 + 300 + ($receipts - 1500) * 0.1" | bc)
fi

# Small day-based adjustments
day_adjustment=0
if [ "$days" -eq 5 ]; then
    day_adjustment=25
elif [ "$days" -ge 10 ]; then
    day_adjustment=-20
fi

total=$(echo "scale=2; $base_amount + $mileage_amount + $receipt_amount + $day_adjustment" | bc)

printf "%.2f\n" $total