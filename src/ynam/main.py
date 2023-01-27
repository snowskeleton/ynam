import signal
import sys
import os

from .mint_api import MintAPI
from .ynab_api import YNABAPI
from .ynam_parser import arg, logger
from .ynam_secrets import get_stash


def signal_handler(sig, frame):
    sys.exit(print('\nynam: received SIGINT. exit 1'))


signal.signal(signal.SIGINT, signal_handler)


def main():
    handleArgs()
    validate_files()

    mint_api = MintAPI()
    try:
        mint_transactions = mint_api.get_transactions(start_date=arg('days'))
    except Exception:
        mint_api.updateAuth()
        mint_transactions = mint_api.get_transactions(start_date=arg('days'))

    stash = get_stash()
    ynab_api = YNABAPI(stash.ynab_api_key)
    ynab_api.budget_id = stash.ynab_budget_id
    ynab_transactions = ynab_api.get_account_transactions(
        stash.ynab_account_id)

    ynab_ids = [y.import_id for y in ynab_transactions]
    ynab_ids = [
        mint.asYNAB() for mint in mint_transactions if mint.id not in ynab_ids]
    ynab_ids = [nab.asdict() for nab in ynab_ids]

    if arg('dryrun'):
        sys.exit(print(ynab_ids))

    if len(ynab_ids) > 0:
        result = ynab_api.post_transactions(ynab_ids)
        # TODO: parse through the results a bit to give better data.
        # e.g., X many transactions, across N days, etc.
        logger.info(result)


def handleArgs():
    if arg('deviate'):
        from .ynam_parser import migrate_v0_3_4_0
        migrate_v0_3_4_0()
    if arg('print_ynab_transactions'):
        sys.exit(YNABAPI(get_stash().ynab_api_key).print_transactions())
    if arg('quickstart'):
        from .quickstart import run
        sys.exit(run())
    if arg('blab'):
        sys.exit(print(get_stash()))
    if arg('update_auth'):
        mapi = MintAPI()
        sys.exit(mapi.updateAuth())


def validate_files():
    from .ynam_parser import migrate_v0_3_4_0
    migrate_v0_3_4_0()

    secrets = arg('secrets_file')
    if not os.path.exists(secrets):
        raise FileNotFoundError(
            f"Missing {secrets}. Create it with `ynam --quickstart`")

    files = [
        arg('mint_api_key_file'),
        arg('mint_cookies'),
        arg('chromedriver'),
        arg('session_file'),
    ]
    for file in files:
        logger.debug(f'Validating {file}...')
        if not os.path.exists(file):
            logger.debug(
                f'{file} does not exist; created empty file in its place.')
            with open(file, 'w'):
                pass


if __name__ == "__main__":
    main()
