# Implementation Plan for Black Box Reimbursement System

## Overview
The goal is to reverse-engineer a 60-year-old travel reimbursement system that takes three inputs:
- `trip_duration_days` (integer)
- `miles_traveled` (integer or float based on some examples)
- `total_receipts_amount` (float)

And outputs a single reimbursement amount (float, rounded to 2 decimal places).

## Key Insights from Employee Interviews

### 1. Base Components
- **Per Diem**: ~$100/day base rate (Lisa)
- **Mileage**: Tiered system, ~$0.58/mile for first 100 miles, then drops (Lisa)
- **Receipts**: Complex processing with diminishing returns and penalties

### 2. Special Rules & Bonuses
- **5-day trips**: Consistent bonus (Lisa, Marcus)
- **Efficiency bonus**: 180-220 miles/day is optimal (Kevin)
- **Trip length sweet spot**: 4-6 days generally better (Jennifer, Marcus)

### 3. Penalties
- **Small receipts**: <$50 can be worse than $0 (Lisa, Jennifer)
- **High spending on long trips**: >$90/day on 8+ day trips (Kevin)
- **Very high receipts**: Diminishing returns kick in

### 4. Edge Cases & Quirks
- Receipt amounts ending in .49 or .99 might get special treatment (Lisa)
- Possible seasonal/timing variations (Kevin's Tuesday/lunar theories)
  - Since the public cases do not include dates, this cannot be a factor
- System might have different calculation paths based on trip type

## Implementation Strategy

### Phase 1: Data Analysis
1. **Extract patterns from public_cases.json**:
   - Group by trip duration to identify duration-specific rules
   - Analyze mileage tiers and breakpoints
   - Study receipt processing patterns
   - Look for efficiency bonuses (miles/day ratios)

2. **Identify calculation paths**:
   - Short trips (1-3 days)
   - Medium trips (4-6 days)
   - Long trips (7+ days)
   - High efficiency vs low efficiency
   - High spending vs low spending

### Phase 2: Core Calculation Components

#### A. Base Per Diem Calculation
```
base_per_diem = trip_duration_days * base_rate
- Identify base_rate (likely ~$100)
- Check for duration-specific adjustments
- Special bonus for 5-day trips
```

#### B. Mileage Calculation
```
mileage_reimbursement = tiered_mileage_calc(miles_traveled)
- First tier: 0-100 miles at ~$0.58/mile
- Subsequent tiers with decreasing rates
- Possible logarithmic or curved decrease
```

#### C. Receipt Processing
```
receipt_adjustment = process_receipts(total_receipts_amount, trip_duration_days)
- Penalties for very low amounts
- Diminishing returns for high amounts
- Sweet spots around $600-800 (medium-high)
- Consider daily spending rate (receipts/days)
```

#### D. Efficiency Bonus/Penalty
```
efficiency = miles_traveled / trip_duration_days
- Bonus for 180-220 miles/day
- Penalties for extremes (too low or too high)
```

### Phase 3: Special Cases & Adjustments

1. **Trip Duration Modifiers**:
   - 5-day bonus
   - Possible penalties for very long trips (12+ days)
   - Different calculation paths by duration

2. **Spending Pattern Adjustments**:
   - Daily spending thresholds by trip length
   - Interaction between receipts and trip duration

3. **Edge Case Handling**:
   - Receipt rounding (.49, .99 endings)
   - Zero or near-zero values
   - Extreme values (very high miles, receipts)

### Phase 4: Implementation Approach

Since we can only use bash scripting, the implementation will:

1. **Use bc for floating-point arithmetic** (already used in eval.sh)
2. **Implement conditional logic** for different calculation paths
3. **Create functions** for:
   - Tiered mileage calculation
   - Receipt processing with penalties/bonuses
   - Efficiency calculations
   - Duration-based adjustments

4. **Test iteratively** against public_cases.json to refine parameters

### Phase 5: Parameter Tuning

1. **Start with baseline estimates** from interviews
2. **Use public_cases.json to**:
   - Fine-tune tier breakpoints
   - Adjust bonus/penalty thresholds
   - Calibrate interaction effects

3. **Focus on high-error cases** to identify missing rules

## Testing Strategy

1. **Group test cases** by characteristics:
   - Trip duration buckets
   - Efficiency levels
   - Receipt amount ranges

2. **Identify patterns** in failures:
   - Consistent over/under estimation
   - Specific scenarios with high error

3. **Iterative refinement**:
   - Adjust parameters based on error patterns
   - Add special case handling as needed

## Expected Challenges

1. **Complex interactions**: Multiple factors affect each other
2. **Hidden rules**: Some patterns might only be visible in specific combinations
3. **Precision requirements**: Need exact matches within $0.01
4. **Potential bugs**: System quirks that need to be replicated

## Success Metrics

- Achieve 95%+ exact matches (±$0.01)
- Minimize average error
- Handle all edge cases properly
- Complete implementation in bash only

## Next Steps

1. Create initial bash script with basic structure
2. Implement core calculation components
3. Analyze public_cases.json for patterns
4. Iteratively refine based on test results
5. Focus on high-error cases for final adjustments

## Additional Data Insights from public_cases.json

### Dataset Composition
- **5-day trips**: 112 cases (11.2% of dataset) - significant representation for testing the 5-day bonus
- **Receipt endings**: 
  - 16 cases end in .49
  - 14 cases end in .99
  - Total of 30 cases (3%) to test the rounding hypothesis

### Efficiency Patterns
- **Extreme efficiency cases**: Single-day trips with 1000+ miles show that the system handles extreme efficiency
- **Examples of very high efficiency**:
  - 1166 miles/day: $1423.69 receipts → $1412.13 reimbursement
  - 1122 miles/day: $861.50 receipts → $1081.05 reimbursement
  - These suggest the system might cap efficiency bonuses or apply penalties for unrealistic travel

### Initial Observations for Implementation
1. **5-day bonus validation**: With 112 cases, we can accurately determine the 5-day bonus amount
2. **Receipt rounding**: 30 test cases to verify the .49/.99 rounding rule
3. **Efficiency handling**: Need to handle extreme cases (1000+ miles/day) appropriately
4. **Range of values**:
   - Trip duration: 1-14 days
   - Miles: 0-1200+
   - Receipts: $0-2500+

### Testing Priorities
1. Start with simple cases (low values, round numbers)
2. Test 5-day trips separately to isolate the bonus
3. Verify efficiency calculations with extreme cases
4. Check receipt rounding with the 30 special cases
5. Validate against edge cases (zero miles, zero receipts, etc.) 