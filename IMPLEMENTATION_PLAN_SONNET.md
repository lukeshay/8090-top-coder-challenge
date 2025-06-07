# Implementation Plan: Black Box Legacy Reimbursement System

## Problem Summary

We need to reverse-engineer a 60-year-old travel reimbursement system by analyzing 1,000 historical input/output examples and employee interviews. The system takes three inputs:
- `trip_duration_days` (integer) 
- `miles_traveled` (integer)
- `total_receipts_amount` (float)

And outputs a single reimbursement amount (float, rounded to 2 decimal places).

## Key Insights from Employee Interviews

### From Lisa (Accounting):
- Base per diem appears to be ~$100/day
- 5-day trips get a consistent bonus (except in some cases)
- Mileage is tiered: first ~100 miles at full rate (~$0.58/mile), then drops off in a curve
- Receipt processing has diminishing returns: $600-800 gets good treatment, higher amounts penalized
- Very low receipts (<$50) often worse than submitting nothing
- Certain receipt amounts ending in .49 or .99 get rounding bonuses (possible bug)

### From Kevin (Procurement - has extensive data):
- 6 different calculation paths based on trip characteristics
- Efficiency rewards: 180-220 miles/day is the sweet spot
- Optimal spending ranges by trip length:
  - Short trips: <$75/day
  - Medium trips (4-6 days): <$120/day  
  - Long trips: <$90/day
- "Sweet spot combo": 5-day trips + 180+ miles/day + <$100/day spending = guaranteed bonus
- "Vacation penalty": 8+ day trips with high spending = penalty
- High mileage + low spending = usually good
- Low mileage + high spending = usually bad

### From Marcus (Sales):
- Unpredictable variations for seemingly identical trips
- 8-day high-mileage trips can get "incredible" reimbursements
- 600-mile trips got less than expected per-mile rate
- End of Q4 more generous
- Possible monthly quotas or timing effects

### From Jennifer (HR):
- 4-6 day trips have a "sweet spot" for reimbursements
- New employees tend to get lower reimbursements initially
- Different departments may have different treatment

## Data Analysis Strategy

### Phase 1: Basic Pattern Recognition
1. **Per Diem Base Analysis**
   - Look for base rates around $100/day
   - Identify 5-day trip bonuses
   - Check for trip length penalties/bonuses

2. **Mileage Rate Analysis**
   - Identify the basic rate (likely ~$0.58/mile for first 100 miles)
   - Map the diminishing returns curve for higher mileage
   - Test efficiency bonuses (miles/day ratios)

3. **Receipt Processing Analysis**
   - Identify optimal spending ranges
   - Map diminishing returns for high spending
   - Check for low-spending penalties
   - Test rounding effects (.49/.99 endings)

### Phase 2: Advanced Pattern Detection
1. **Interaction Effects**
   - Trip length × efficiency interactions
   - Spending per day × total mileage interactions
   - Multiple threshold effects

2. **Calculation Path Identification**
   - Cluster similar trip types
   - Identify the 6 different calculation paths Kevin mentioned
   - Map which conditions trigger which paths

3. **Edge Case Analysis**
   - Very short trips (1 day)
   - Very long trips (8+ days)
   - Very high mileage (800+ miles)
   - Very low/high spending amounts

## Implementation Approach

### Tools Available:
- `jq` for JSON parsing
- `bc` for floating-point arithmetic
- Standard bash scripting
- Cannot call external scripts

### Recommended Implementation:
**Bash script with `bc` for calculations** - This keeps everything self-contained and fast.

### Algorithm Structure:

```bash
#!/bin/bash

# Input parameters
trip_duration=$1
miles_traveled=$2
total_receipts=$3

# Base calculation components:
# 1. Base per diem calculation
# 2. Mileage calculation with tiers
# 3. Receipt processing with caps/penalties
# 4. Efficiency bonuses
# 5. Trip length modifiers
# 6. Special case handling

# Base per diem (starts at ~$100/day)
base_per_diem=$(echo "scale=2; $trip_duration * 100" | bc)

# Mileage calculation (tiered)
if [ $miles_traveled -le 100 ]; then
    mileage_reimbursement=$(echo "scale=2; $miles_traveled * 0.58" | bc)
else
    # First 100 miles at full rate, rest at reduced rate
    # Need to determine the exact curve from data analysis
fi

# Receipt processing
# Need to implement the diminishing returns curve

# Efficiency bonus calculation
miles_per_day=$(echo "scale=2; $miles_traveled / $trip_duration" | bc)
# Apply bonuses for 180-220 miles/day range

# Trip length modifiers
# 5-day bonus, 8+ day penalties, etc.

# Combine all components and apply any final adjustments
final_amount=$(echo "scale=2; $base_per_diem + $mileage_reimbursement + $receipt_adjustment + $efficiency_bonus + $trip_modifier" | bc)

echo $final_amount
```

## Development Process

### Step 1: Data Exploration Script
Create a bash script that analyzes the public_cases.json to identify:
- Average reimbursement per day by trip length
- Mileage rates by distance brackets
- Receipt treatment by amount ranges
- Efficiency patterns

### Step 2: Initial Implementation
Based on data exploration, create a basic implementation covering:
- Base per diem (~$100/day)
- Tiered mileage rates
- Basic receipt processing
- 5-day trip bonus

### Step 3: Iterative Refinement
Use `./eval.sh` to test and refine:
- Analyze high-error cases
- Adjust parameters based on feedback
- Add more sophisticated interaction effects
- Handle edge cases

### Step 4: Advanced Features
Implement the more complex patterns:
- Multiple calculation paths
- Efficiency bonuses
- Interaction effects
- Special cases and "bugs"

## Key Parameters to Discover Through Analysis

1. **Base per diem rate** (likely ~$100)
2. **Mileage rates and breakpoints** (likely $0.58 for first 100 miles)
3. **Receipt processing curve** (optimal range $600-800)
4. **5-day trip bonus amount**
5. **Efficiency bonus thresholds** (180-220 miles/day)
6. **Spending limits by trip length**
7. **Long trip penalties** (8+ days)
8. **Rounding effects** (.49/.99 bonuses)

## Success Metrics

- Target: >95% exact matches (within $0.01)
- Minimum: >80% exact matches for initial implementation
- Use high-error cases from eval.sh to guide improvements

## Risk Mitigation

1. **Start simple**: Get basic per diem + mileage working first
2. **Incremental testing**: Test each component addition
3. **Data-driven**: Let the actual test results guide parameter tuning
4. **Pattern validation**: Cross-reference findings with interview insights
5. **Edge case handling**: Specifically test the boundary conditions mentioned in interviews

This approach balances the systematic analysis Kevin suggests with the practical insights from other employees, while remaining implementable in bash with the available tools. 