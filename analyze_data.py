#!/usr/bin/env python3

import json
import math
from collections import defaultdict

# Load the public cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print(f"Total cases: {len(cases)}")

# Basic statistics
trip_durations = [case['input']['trip_duration_days'] for case in cases]
miles_traveled = [case['input']['miles_traveled'] for case in cases]
receipts = [case['input']['total_receipts_amount'] for case in cases]
outputs = [case['expected_output'] for case in cases]

print(f"\nTrip Duration - Min: {min(trip_durations)}, Max: {max(trip_durations)}, Avg: {sum(trip_durations)/len(trip_durations):.1f}")
print(f"Miles - Min: {min(miles_traveled)}, Max: {max(miles_traveled)}, Avg: {sum(miles_traveled)/len(miles_traveled):.1f}")
print(f"Receipts - Min: {min(receipts):.2f}, Max: {max(receipts):.2f}, Avg: {sum(receipts)/len(receipts):.1f}")
print(f"Output - Min: {min(outputs):.2f}, Max: {max(outputs):.2f}, Avg: {sum(outputs)/len(outputs):.1f}")

# Group by trip duration
duration_groups = defaultdict(list)
for i, case in enumerate(cases):
    duration = case['input']['trip_duration_days']
    duration_groups[duration].append(i)

print(f"\nTrip duration distribution:")
for duration in sorted(duration_groups.keys()):
    print(f"  {duration} days: {len(duration_groups[duration])} cases")

# Let's look at some simple patterns
# Base per diem calculation check
print(f"\nAnalyzing base per diem patterns...")
for duration in [1, 2, 3, 4, 5]:
    if duration in duration_groups:
        subset = [cases[i] for i in duration_groups[duration][:10]]  # First 10 cases
        print(f"\n{duration}-day trips (sample):")
        for case in subset:
            days = case['input']['trip_duration_days']
            miles = case['input']['miles_traveled']
            receipts = case['input']['total_receipts_amount']
            output = case['expected_output']
            
            # Calculate miles per day
            miles_per_day = miles / days if days > 0 else 0
            
            print(f"  Days: {days}, Miles: {miles}, Receipts: ${receipts:.2f}, Output: ${output:.2f}, Miles/day: {miles_per_day:.1f}")

# Create simple groups for incremental development
simple_cases = []
medium_cases = []
complex_cases = []

for i, case in enumerate(cases):
    days = case['input']['trip_duration_days']
    miles = case['input']['miles_traveled']
    receipts = case['input']['total_receipts_amount']
    
    # Simple: short trips, low mileage, low receipts
    if days <= 2 and miles <= 100 and receipts <= 50:
        simple_cases.append(case)
    # Complex: long trips, high mileage, or high receipts
    elif days >= 7 or miles >= 500 or receipts >= 500:
        complex_cases.append(case)
    else:
        medium_cases.append(case)

print(f"\nGrouping summary:")
print(f"Simple cases: {len(simple_cases)}")
print(f"Medium cases: {len(medium_cases)}")
print(f"Complex cases: {len(complex_cases)}")

# Save groups to files
with open('groups/simple.json', 'w') as f:
    json.dump(simple_cases, f, indent=2)

with open('groups/medium.json', 'w') as f:
    json.dump(medium_cases, f, indent=2)

with open('groups/complex.json', 'w') as f:
    json.dump(complex_cases, f, indent=2)

print(f"\nSaved groups to groups/ directory")