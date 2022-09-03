#!/usr/bin/env python3
from utils import YNABTransaction, allTransactions
from api import postTransaction


def main():
    transactions = allTransactions()
    for transaction in transactions:
        transaction = YNABTransaction(transaction)
        postTransaction(transaction)


if __name__ == "__main__":
    main()
