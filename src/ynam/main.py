from .utils import YNABTransaction, allTransactions
from .api import postTransaction
from .parser import parse


def run():
    parse()

    transactions = allTransactions()
    for transaction in transactions:
        transaction = YNABTransaction(transaction)
        postTransaction(transaction)


if __name__ == "__main__":
    run()
