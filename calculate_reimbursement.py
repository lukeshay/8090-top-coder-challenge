#!/usr/bin/env python3
import sys, math

# Precomputed coefficients from least squares fit on public_cases.json
COEFFS = [
    65.65546448519353,
    496.7780836462639,
    -2.566982455107375,
    8.984500849624599,
    -36.34551091953301,
    0.002339381383841216,
    -0.0025392138949094584,
    0.007930405016133023,
    -0.0036984732715396457,
    -7.972586059545171e-05,
    1.1819249149979163,
    -9.495667452134273e-07,
    3.5133330720701754e-07,
    -8.01453019108394e-06,
    -321.41521867560704,
    83.68790598754897,
    -298.2404582940148,
    -498.89726563273297,
    -146.25848780865616,
    539.8177220020503,
    -0.19774000603406003,
    0.039155990964753626,
    -0.16176156116695117,
]

def calculate(td, mi, re):
    td = float(td)
    mi = float(mi)
    re = float(re)
    features = [
        1,
        td,
        mi,
        re,
        td ** 2,
        mi ** 2,
        re ** 2,
        td * mi,
        td * re,
        mi * re,
        td ** 3,
        mi ** 3,
        re ** 3,
        td * mi * re,
        math.sqrt(td),
        math.sqrt(mi),
        math.sqrt(re),
        math.log(td + 1),
        math.log(mi + 1),
        math.log(re + 1),
        (mi / td) if td != 0 else 0,
        (re / td) if td != 0 else 0,
        (re / mi) if mi != 0 else 0,
    ]
    assert len(features) == len(COEFFS)
    value = sum(c * f for c, f in zip(COEFFS, features))
    return round(value, 2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: calculate_reimbursement.py <days> <miles> <receipts>")
        sys.exit(1)
    result = calculate(float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]))
    # Output just the number with two decimal places
    print(f"{result:.2f}")
