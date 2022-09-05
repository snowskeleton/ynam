from .utils import YNABTransaction, allTransactions
from .api import postTransaction


def main():
    transactions = allTransactions()
    for transaction in transactions:
        transaction = YNABTransaction(transaction)
        postTransaction(transaction)
