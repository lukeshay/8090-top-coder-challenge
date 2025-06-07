#!/usr/bin/env python3
import sys
from itertools import combinations_with_replacement

def main():
    if len(sys.argv)!=4:
        print("0")
        return
    days=float(sys.argv[1])
    miles=float(sys.argv[2])
    receipts=float(sys.argv[3])

    mean=[7.043,597.41374,1211.05687]
    std=[3.9241752,351.12409597,742.48266037]
    vars=[(days-mean[0])/std[0],(miles-mean[1])/std[1],(receipts-mean[2])/std[2]]
    coeffs=[1600.416384072401,130.72748193408887,204.87253463802793,391.473534124483,-61.04381759361258,19.35298597362796,-35.613367408490056,50.09751928892022,-89.29225585754673,-380.4334787275347,27.363077666460494,-19.81784212097141,12.184134703964846,25.53068816919307,-9.922200908215107,-7.080106149795828,-9.505379155171886,4.636042085968149,-19.970682600356177,-67.80858522373693,7.732051794685229,-8.739538014005053,6.4000630107503484,-11.74766832602759,-0.6670124637728709,2.4052931070759227,11.281133992702518,1.5933916123858152,-8.436426382649282,-5.834585468051751,-5.730224078030806,4.839197375011675,-27.996819522585294,27.391063042726934,105.93860352093486]
    feats=[1.0]
    for deg in range(1,5):
        for combo in combinations_with_replacement(range(3),deg):
            val=1.0
            for idx in combo:
                val*=vars[idx]
            feats.append(val)
    base=sum(c*f for c,f in zip(coeffs,feats))

    cents=round(receipts-int(receipts),2)
    if abs(cents-0.49)<0.01 or abs(cents-0.99)<0.01:
        base+=-477.11692186827014

    print(f"{base:.2f}")

if __name__=="__main__":
    main()
