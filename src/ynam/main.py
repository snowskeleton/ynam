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

    ynab = ynapi.getTransactions()
    mints = mapi.dispenseMints()

    transactions = []
    for mint in mints:
        if mint['id'] not in [y['import_id'] for y in ynab]:
            transactions.append(MintAPI.asYNAB(mint))

    if not arg('dryrun') and len(transactions) > 0:
        if arg('verbose'):
            print(f'Posting {len(transactions)} transactions to YNAB')
        ynapi.bulkPostTransactions(transactions)


def handleArgs():
    if arg('quickstart'):
        from .quickstart import run
        run()
        sys.exit(0)
    if arg('blab'):
        # Uncomment if you want to be unsafe.
        from .utils import stash
        for key in [
                'api_key',
                'username',
                'password',
                'account_id',
                'budget_id',
                'mfa_seed_token',
        ]:
            print(f'{key}: {stash.valueOf(key)}')
        sys.exit(0)
    if arg('update_auth'):
        mapi = MintAPI()
        mapi.updateAuth()
        sys.exit(0)


if __name__ == "__main__":
    main()
