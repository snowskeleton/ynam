from dataclasses import asdict
import signal
import sys

from .api import MintAPI, YNABAPI
from .parser import arg


def signal_handler(sig, frame):
    sys.exit(print('\nynam: received SIGINT. exit 1'))


signal.signal(signal.SIGINT, signal_handler)


def main():
    handleArgs()
    ynapi = YNABAPI()
    mapi = MintAPI()

    ydeez = [y.import_id for y in ynapi.getTransactions()]
    nabs = [
        asdict(mint.asYNAB()) for mint in mapi.freshMints()
        if mint.id not in ydeez
    ]
    if arg('verbose'):
        print(nabs)
    if not arg('dryrun') and len(nabs) > 0:
        ynapi.bulkPostTransactions(nabs)


def handleArgs():
    if arg('print_ynab_transactions'):
        sys.exit(YNABAPI().printTransactions())
    if arg('quickstart'):
        from .quickstart import run
        sys.exit(run())
    if arg('blab'):
        from .secrets import stash
        sys.exit(print(stash))
    if arg('update_auth'):
        mapi = MintAPI()
        sys.exit(mapi.updateAuth())


if __name__ == "__main__":
    main()
