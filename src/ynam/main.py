import sys
import signal
import sys
from .mint_api import dispenseMints
from .ynab_api import postTransaction as post
from .parser import arg


def signal_handler(sig, frame):
    sys.exit(print('\nynam: received SIGINT. exit 1'))


signal.signal(signal.SIGINT, signal_handler)


def main():

    if arg('quickstart'):
        from .quickstart import run
        run()
        sys.exit(0)

    transactions = dispenseMints()
    for transaction in transactions:
        post(transaction) if not arg('dryrun') else print(transaction)


if __name__ == "__main__":
    main()
