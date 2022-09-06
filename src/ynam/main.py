from .utils import getTransactions
from .api import postTransaction as post
from .parser import arg


def run():
    if arg('quickstart'):
        from .quickstart import run
        run()

    transactions = getTransactions()
    for transaction in transactions:
        post(transaction) if not arg('dryrun') else print(transaction)

if __name__ == "__main__":
    run()
