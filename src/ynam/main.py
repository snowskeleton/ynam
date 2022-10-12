import signal
import sys
import ast

from .mint_api import dispenseMints
from .ynab_api import postTransaction as post, getTransactions as get
from .parser import arg
from .utils import mintToYnab, stash


def signal_handler(sig, frame):
    sys.exit(print('\nynam: received SIGINT. exit 1'))


signal.signal(signal.SIGINT, signal_handler)


def main():
    handleArgs()

    mints = dispenseMints(fromFile(arg('cookies')),
                          fromFile(arg('key'))['authorization'])
    ynab = get(stash.valueOf('budget_id'), "2022-09-16", "None")

    nabs = [y['import_id'] for y in ynab]
    transactions = []
    for mint in mints:
        if mint['id'] not in nabs:
            transactions.append(mintToYnab(mint))

    for t in transactions:
        if not arg('dryrun'):
            post(stash.valueOf('budget_id'), t)
        else:
            print(t)


def handleArgs():
    if arg('quickstart'):
        from .quickstart import run
        run()
        sys.exit(0)
    if arg('blab'):
        ## Uncomment if you want to be unsafe.
        # from .config import valueOf
        # for key in [
        #         'api_key',
        #         'username',
        #         'password',
        #         'account_id',
        #         'budget_id',
        #         'mfa_seed_token',
        # ]:
        #     print(f'{key}: {valueOf(key)}')
        print('check the code')
        sys.exit(0)
    if arg('update_auth'):
        from .quickstart import updateAuth
        updateAuth()
        sys.exit(0)


def fromFile(file):
    with open(file) as file:
        return ast.literal_eval(file.read())


if __name__ == "__main__":
    main()
