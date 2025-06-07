import sys

COEFFS = [
    -165.13884827175676,
    88.17230215711506,
    0.40695501109991317,
    1.2116765573769879,
    -2.5902746074911858,
    3.526925506198016e-05,
    -0.0002785201970961713,
    0.014510187774861268,
    -0.008909396689417523,
    -0.00011392118366839193,
]

def compute(days, miles, receipts):
    features = [
        1,
        days,
        miles,
        receipts,
        days ** 2,
        miles ** 2,
        receipts ** 2,
        days * miles,
        days * receipts,
        miles * receipts,
    ]
    result = sum(c * f for c, f in zip(COEFFS, features))
    return round(result, 2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 calculate_reimbursement.py <days> <miles> <receipts>")
        sys.exit(1)
    days = float(sys.argv[1])
    miles = float(sys.argv[2])
    receipts = float(sys.argv[3])
    output = compute(days, miles, receipts)
    print(f"{output:.2f}")
