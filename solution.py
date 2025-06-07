#!/usr/bin/env python3
import sys
from arrays import FEATURES, THRESHOLDS, LEFT, RIGHT, VALUES

def predict(days, miles, receipts):
    node = 0
    while True:
        feature = FEATURES[node]
        if feature == -2:
            return VALUES[node]
        value = (days, miles, receipts)[feature]
        if value <= THRESHOLDS[node]:
            node = LEFT[node]
        else:
            node = RIGHT[node]

def main():
    if len(sys.argv) != 4:
        print("0")
        return
    days = float(sys.argv[1])
    miles = float(sys.argv[2])
    receipts = float(sys.argv[3])
    print(f"{predict(days, miles, receipts):.2f}")

if __name__ == "__main__":
    main()
