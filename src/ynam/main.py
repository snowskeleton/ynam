#!/usr/bin/env python3
import argparse
from utils import YNABTransaction, allTransactions
from api import postTransaction


def main():
    transactions = allTransactions()
    for transaction in transactions:
        transaction = YNABTransaction(transaction)
        postTransaction(transaction)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description='You Need a Mint (connection)')
    p.add_argument('-q, --quickstart',
                   dest='q',
                   action='store_true',
                   help='A required integer positional argument')
    args = p.parse_args()
    if args.q:
        from quickstart import run
        run()

    main()
