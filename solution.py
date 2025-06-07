#!/usr/bin/env python3

import sys
import math

def calculate_reimbursement(trip_duration_days, miles_traveled, total_receipts_amount):
    """
    Calculate reimbursement using balanced approach with caps and safeguards.
    
    Based on analysis: $100/day + $0.58/mile works well as baseline,
    but needs careful adjustments for extremes.
    """
    days = int(trip_duration_days)
    miles = float(miles_traveled)
    receipts = float(total_receipts_amount)
    
    # Proven baseline
    base_calculation = days * 100 + miles * 0.58
    
    # Receipt adjustments with safeguards against over-corrections
    receipt_adjustment = 0
    receipts_per_day = receipts / days if days > 0 else 0
    
    if receipts < 50:
        # Small penalty for very low receipts
        receipt_adjustment = -10 * days
    elif receipts_per_day > 500:
        # Cap bonuses for extremely high per-day spending
        if days >= 8:
            # Long trips with high spending get penalized
            receipt_adjustment = max(0, (receipts - 500) * 0.1)
        else:
            # Short trips with high spending get good bonuses
            receipt_adjustment = (receipts - 500) * 0.5
    elif receipts > 1000:
        # High receipts get good bonus but capped
        receipt_adjustment = min((receipts - 1000) * 0.4, 400)
    elif receipts > 500:
        # Medium-high receipts
        receipt_adjustment = (receipts - 500) * 0.2
    elif receipts > 200:
        # Medium receipts
        receipt_adjustment = (receipts - 200) * 0.08
    
    # Trip length penalties
    trip_penalty = 0
    if days >= 12:
        trip_penalty = (days - 11) * 25
    elif days >= 8:
        trip_penalty = (days - 7) * 12
    
    # Efficiency considerations
    miles_per_day = miles / days if days > 0 else 0
    efficiency_adjustment = 0
    
    if miles_per_day > 400:
        # Penalty for extremely high daily mileage
        efficiency_adjustment = -20 * days
    elif 180 <= miles_per_day <= 220:
        # Sweet spot bonus
        efficiency_adjustment = 15 * days
    
    # Special case adjustments for common patterns
    special_adjustment = 0
    
    # 5-day trip bonus (mentioned in interviews)
    if days == 5:
        special_adjustment += 10
    
    # Calculate final reimbursement
    total = (base_calculation + receipt_adjustment - trip_penalty + 
             efficiency_adjustment + special_adjustment)
    
    return round(total, 2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 solution.py <trip_duration_days> <miles_traveled> <total_receipts_amount>")
        sys.exit(1)
    
    try:
        trip_duration = sys.argv[1]
        miles = sys.argv[2] 
        receipts = sys.argv[3]
        
        result = calculate_reimbursement(trip_duration, miles, receipts)
        print(result)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)