from decimal import Decimal, getcontext
getcontext().prec = 28

# Coefficients from polynomial regression of degree 4 on public cases
INTERCEPT = 293.60508953664976
COEFFS = [
    4.109345164419563e-06,
    0.006304625090316324,
    -0.09346570480176015,
    -0.8489208633567166,
    0.06677153089874359,
    0.25215753373821985,
    0.09482731340969432,
    0.0008114764150438377,
    -0.0007073112014215874,
    0.002871281131826774,
    0.46154868790991566,
    -0.01146689748041218,
    -0.012172175216802195,
    -0.00020133260904282713,
    -5.0288409906853536e-05,
    -5.349652591251255e-06,
    -3.449009779436357e-07,
    9.259346293532062e-07,
    8.251013257217014e-08,
    -1.7827459469687747e-06,
    -0.017569769568300358,
    4.9721376165924064e-05,
    0.0003556267307790735,
    9.249129381799841e-07,
    2.892159280941891e-06,
    1.2572027163708195e-06,
    1.1349005606692717e-07,
    1.743554552433811e-08,
    -1.0522158691506348e-08,
    -2.7134026319537205e-09,
    -3.4212104489538794e-10,
    1.1251332819748475e-10,
    -4.8829394202067464e-10,
    1.3648854919807894e-10,
    3.241261575888556e-10,
]

# Feature computation order matches sklearn PolynomialFeatures(4)
def compute(days, miles, receipts):
    d = Decimal(days)
    m = Decimal(miles)
    r = Decimal(receipts)

    feats = [
        Decimal(1),  # constant term
        d,
        m,
        r,
        d**2,
        d*m,
        d*r,
        m**2,
        m*r,
        r**2,
        d**3,
        d**2*m,
        d**2*r,
        d*m**2,
        d*m*r,
        d*r**2,
        m**3,
        m**2*r,
        m*r**2,
        r**3,
        d**4,
        d**3*m,
        d**3*r,
        d**2*m**2,
        d**2*m*r,
        d**2*r**2,
        d*m**3,
        d*m**2*r,
        d*m*r**2,
        d*r**3,
        m**4,
        m**3*r,
        m**2*r**2,
        m*r**3,
        r**4,
    ]

    total = Decimal(INTERCEPT)
    for c, f in zip(COEFFS, feats):
        total += Decimal(c) * f
    return float(total)

if __name__ == '__main__':
    import sys
    d, m, r = sys.argv[1:4]
    result = compute(d, m, r)
    print(f"{result:.2f}")
