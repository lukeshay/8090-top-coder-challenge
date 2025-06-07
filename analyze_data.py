#!/usr/bin/env python3

import json
import os

# Load test cases
with open('public_cases.json', 'r') as f:
    cases = json.load(f)

print(f"Total cases: {len(cases)}")

# Create groups by trip duration first
duration_groups = {}
for i, case in enumerate(cases):
    duration = case['input']['trip_duration_days']
    if duration not in duration_groups:
        duration_groups[duration] = []
    duration_groups[duration].append(case)

print("Cases by duration:")
for duration in sorted(duration_groups.keys()):
    print(f"  {duration} days: {len(duration_groups[duration])} cases")

# Create simple groups for incremental development
os.makedirs('groups', exist_ok=True)

# Group 1: Short trips (1-3 days)
short_trips = []
for duration in [1, 2, 3]:
    if duration in duration_groups:
        short_trips.extend(duration_groups[duration])

with open('groups/short_trips.json', 'w') as f:
    json.dump(short_trips[:50], f, indent=2)  # Start with first 50

print(f"Created short_trips.json with {len(short_trips[:50])} cases")

# Group 2: Medium trips (4-6 days)  
medium_trips = []
for duration in [4, 5, 6]:
    if duration in duration_groups:
        medium_trips.extend(duration_groups[duration])

with open('groups/medium_trips.json', 'w') as f:
    json.dump(medium_trips[:50], f, indent=2)

print(f"Created medium_trips.json with {len(medium_trips[:50])} cases")

# Group 3: 1-day trips only (simpler analysis)
one_day_trips = duration_groups.get(1, [])[:30]
with open('groups/one_day.json', 'w') as f:
    json.dump(one_day_trips, f, indent=2)

print(f"Created one_day.json with {len(one_day_trips)} cases")

# Analyze some basic patterns for 1-day trips
print("\nAnalyzing 1-day trips:")
for case in one_day_trips[:10]:
    inp = case['input']
    out = case['expected_output']
    miles = inp['miles_traveled']
    receipts = inp['total_receipts_amount']
    
    # Basic per-mile calculation
    base_per_day = 100  # From interviews
    mileage_rate = 0.58  # From interviews
    
    estimated_mileage = miles * mileage_rate
    estimated_receipts = receipts
    estimated_total = base_per_day + estimated_mileage + estimated_receipts
    
    print(f"  Miles: {miles}, Receipts: ${receipts:.2f}, Expected: ${out:.2f}, Estimated: ${estimated_total:.2f}") 