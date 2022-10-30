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

    ynabs = [y.import_id for y in ynapi.getTransactions()]
    ynabs = [
        mint.asYNAB() for mint in mapi.freshMints() if mint.id not in ynabs
    ]

    if not arg('dryrun') and len(ynabs) > 0:
        if arg('verbose'):
            print(f'Posting {len(ynabs)} transactions to YNAB')
        ynapi.bulkPostTransactions([asdict(nab) for nab in ynabs])


def handleArgs():
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
