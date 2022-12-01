import signal
import sys

from .mint_api import MintAPI
from .ynab_api import YNABAPI
from .ynam_parser import arg
from .ynam_secrets import stash


def signal_handler(sig, frame):
    sys.exit(print('\nynam: received SIGINT. exit 1'))


signal.signal(signal.SIGINT, signal_handler)


def main():
    handleArgs()
    ynapi = YNABAPI(stash.ynab_api_key)
    ynapi.budget_id = stash.ynab_budget_id
    mapi = MintAPI()

    try:
        mints = mapi.getXtns(start_date=arg('days'))
    except Exception:
        mapi.updateAuth()
        mints = mapi.getXtns(start_date=arg('days'))

    ydeez = [
        y.import_id
        for y in ynapi.get_account_transactions(stash.ynab_account_id)
    ]
    nabs = [mint.asYNAB() for mint in mints if mint.id not in ydeez]
    nabs = [nab.asdict() for nab in nabs]
    if not arg('dryrun') and len(nabs) > 0:
        result = ynapi.post_transactions(nabs)
        if arg('verbose'):
            print(result)


def handleArgs():
    if arg('print_ynab_transactions'):
        sys.exit(YNABAPI(stash.ynab_api_key).print_transactions())
    if arg('quickstart'):
        from .quickstart import run
        sys.exit(run())
    if arg('blab'):
        sys.exit(print(stash))
    if arg('update_auth'):
        mapi = MintAPI()
        sys.exit(mapi.updateAuth())


if __name__ == "__main__":
    main()
