#!/usr/bin/env python3
import sys

def main():
    if len(sys.argv)!=4:
        print("0")
        return
    days=float(sys.argv[1])
    miles=float(sys.argv[2])
    receipts=float(sys.argv[3])

    base=310.8714952295602 + 48.60725308652175*days + 0.43261802007306094*miles + 0.37303220085351724*receipts

    cents=round(receipts-int(receipts),2)
    if abs(cents-0.49)<0.01 or abs(cents-0.99)<0.01:
        base+=-477.11692186827014

    print(f"{base:.2f}")

if __name__=="__main__":
    main()
