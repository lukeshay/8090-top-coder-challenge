#!/bin/bash

# Black Box Challenge - Penalty Matrix Model
# This model uses a hardcoded 2D lookup table based on trip duration and receipt amount.
# This was the best-performing model with a score of ~12270.
# Usage: ./run.sh <trip_duration_days> <miles_traveled> <total_receipts_amount>

python3 -c "
import sys

def calculate_reimbursement(days, miles, receipts):
    # Base formula: $100/day + $0.60/mile + 70% of receipts
    base_amount = (100.0 * days) + (0.60 * miles) + (0.70 * receipts)
    
    penalty = 0
    # Penalty Matrix derived from the 2D analysis (analyze_difference.py)
    if days == 1:
        if receipts < 500: penalty = -160.69
        elif receipts < 1000: penalty = -206.05
        elif receipts < 1500: penalty = -164.72
        elif receipts < 2000: penalty = -451.51
        else: penalty = -672.90
    elif days == 2:
        if receipts < 500: penalty = -187.39
        elif receipts < 1000: penalty = -178.26
        elif receipts < 1500: penalty = -78.15
        elif receipts < 2000: penalty = -353.49
        else: penalty = -780.45
    elif days == 3:
        if receipts < 500: penalty = -198.44
        elif receipts < 1000: penalty = -234.29
        elif receipts < 1500: penalty = -113.74
        elif receipts < 2000: penalty = -416.87
        else: penalty = -820.91
    elif days == 4:
        if receipts < 500: penalty = -230.60
        elif receipts < 1000: penalty = -269.78
        elif receipts < 1500: penalty = -260.00
        elif receipts < 2000: penalty = -433.26
        else: penalty = -827.76
    elif days == 5:
        if receipts < 500: penalty = -248.43
        elif receipts < 1000: penalty = -197.84
        elif receipts < 1500: penalty = -187.71
        elif receipts < 2000: penalty = -499.41
        else: penalty = -863.70
    elif days == 6:
        if receipts < 500: penalty = -268.60
        elif receipts < 1000: penalty = -248.02
        elif receipts < 1500: penalty = -206.76
        elif receipts < 2000: penalty = -539.03
        else: penalty = -852.15
    elif days == 7:
        if receipts < 500: penalty = -268.55
        elif receipts < 1000: penalty = -288.72
        elif receipts < 1500: penalty = -231.64
        elif receipts < 2000: penalty = -561.58
        else: penalty = -971.37
    elif days == 8:
        if receipts < 500: penalty = -423.70
        elif receipts < 1000: penalty = -393.08
        elif receipts < 1500: penalty = -362.32
        elif receipts < 2000: penalty = -830.63
        else: penalty = -1163.35
    elif days == 9:
        if receipts < 500: penalty = -464.57
        elif receipts < 1000: penalty = -502.75
        elif receipts < 1500: penalty = -400.58
        elif receipts < 2000: penalty = -943.23
        else: penalty = -1271.44
    elif days == 10:
        if receipts < 500: penalty = -591.36
        elif receipts < 1000: penalty = -469.96
        elif receipts < 1500: penalty = -456.22
        elif receipts < 2000: penalty = -970.55
        else: penalty = -1220.83
    elif days == 11:
        if receipts < 500: penalty = -556.02
        elif receipts < 1000: penalty = -664.37
        elif receipts < 1500: penalty = -621.54
        elif receipts < 2000: penalty = -907.53
        else: penalty = -1254.37
    elif days == 12:
        if receipts < 500: penalty = -641.92
        elif receipts < 1000: penalty = -615.82
        elif receipts < 1500: penalty = -566.38
        elif receipts < 2000: penalty = -1056.41
        else: penalty = -1416.40
    elif days == 13:
        if receipts < 500: penalty = -691.65
        elif receipts < 1000: penalty = -583.87
        elif receipts < 1500: penalty = -604.39
        elif receipts < 2000: penalty = -974.06
        else: penalty = -1407.34
    elif days == 14:
        if receipts < 500: penalty = -771.24
        elif receipts < 1000: penalty = -805.03
        elif receipts < 1500: penalty = -691.82
        elif receipts < 2000: penalty = -1077.06
        else: penalty = -1495.38
    else: # Fallback for 15+ days
        penalty = -1500 # A reasonable guess based on trend
    
    total = base_amount + penalty
    
    return round(max(0, total), 2)

# Get command line arguments
days = int(sys.argv[1])
miles = float(sys.argv[2])
receipts = float(sys.argv[3])

result = calculate_reimbursement(days, miles, receipts)
print(f'{result:.2f}')
" "$1" "$2" "$3" 