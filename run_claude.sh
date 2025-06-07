#!/bin/bash

# Back to best performing approach with refinements

days=$1
miles=$2
receipts=$3

# Base per diem - conservative
base_per_diem=$(echo "scale=2; $days * 75" | bc)

# Tiered mileage with smaller rates
if [ $(echo "$miles <= 50" | bc) -eq 1 ]; then
    mileage_total=$(echo "scale=2; $miles * 4.0" | bc)
elif [ $(echo "$miles <= 200" | bc) -eq 1 ]; then
    mileage_total=$(echo "scale=2; $miles * 1.7" | bc)
elif [ $(echo "$miles <= 500" | bc) -eq 1 ]; then
    mileage_total=$(echo "scale=2; $miles * 1.3" | bc)
elif [ $(echo "$miles <= 800" | bc) -eq 1 ]; then
    mileage_total=$(echo "scale=2; $miles * 1.0" | bc)
else
    mileage_total=$(echo "scale=2; $miles * 0.6" | bc)
fi

# Receipt processing with efficiency consideration
efficiency=$(echo "scale=1; $miles / $days" | bc)

if [ $(echo "$days >= 8 && $receipts > 1500" | bc) -eq 1 ]; then
    # Strong vacation penalty only for very long trips + very high receipts
    receipt_bonus=$(echo "scale=2; $receipts * 0.01" | bc)
elif [ $(echo "$days >= 8 && $receipts > 1000" | bc) -eq 1 ]; then
    # Moderate penalty for long trips + high receipts
    receipt_bonus=$(echo "scale=2; $receipts * 0.08" | bc)
elif [ $(echo "$receipts > 2000 && $efficiency < 20" | bc) -eq 1 ]; then
    # Very high receipts + very low efficiency = gets different treatment based on days
    if [ "$days" -le 5 ]; then
        # Short trips with low efficiency and high receipts = severe penalty
        receipt_bonus=$(echo "scale=2; $receipts * 0.02" | bc)
    else
        # Longer trips still get reasonable treatment
        receipt_bonus=$(echo "scale=2; $receipts * 0.3" | bc)
    fi
elif [ $(echo "$receipts > 2000" | bc) -eq 1 ]; then
    # Very high receipts with decent efficiency
    receipt_bonus=$(echo "scale=2; $receipts * 0.35" | bc)
elif [ $(echo "$receipts > 1500 && $efficiency < 100" | bc) -eq 1 ]; then
    # High receipts + medium efficiency = moderate penalty
    receipt_bonus=$(echo "scale=2; $receipts * 0.1" | bc)
elif [ $(echo "$receipts > 1000" | bc) -eq 1 ]; then
    # High receipts get good treatment unless penalized above
    receipt_bonus=$(echo "scale=2; $receipts * 0.3" | bc)
elif [ $(echo "$receipts < 50" | bc) -eq 1 ]; then
    receipt_bonus=$(echo "scale=2; $receipts * 0.1" | bc)
elif [ $(echo "$receipts < 200" | bc) -eq 1 ]; then
    receipt_bonus=$(echo "scale=2; $receipts * 0.3" | bc)
elif [ $(echo "$receipts < 500" | bc) -eq 1 ]; then
    receipt_bonus=$(echo "scale=2; $receipts * 0.25" | bc)
else
    # Medium-high receipts
    receipt_bonus=$(echo "scale=2; $receipts * 0.2" | bc)
fi

total=$(echo "scale=2; $base_per_diem + $mileage_total + $receipt_bonus" | bc)

printf "%.2f\n" $total