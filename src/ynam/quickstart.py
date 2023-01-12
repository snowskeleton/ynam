from getpass import getpass

from .ynab_api import YNABAPI
from .ynam_secrets import stash, updateStash
from .ynam_parser import logger


def safeInput(cap):
    """guarantees int from user input
    """
    logger.debug(f'Querying user for number {cap} or less')
    ans = int(input(f'Enter 1–{cap}: '))
    if ans and ans <= cap:
        logger.debug(f'User entered: {ans}')
        return ans
    else:
        logger.info('Supplied value outside of range.')
        return safeInput(cap)


def usersChoice(items):
    if len(items) == 1:
        print(f"{items[0]['name']}")
        print('Default to only option')
        return items[0]
    else:
        for item in items:
            print(items.index(item) + 1, item['name'])
        selection = safeInput(len(items))
        item = items[int(selection) - 1]
        logger.debug(f'Selected {item} at position {selection}')

        print('selected:', item['name'])
        return item


def run():
    logger.debug('Asking for mint_username')
    username = input('Mint username: ')
    updateStash('mint_username', username.strip())

    logger.debug('Asking for mint_password')
    password = getpass('Mint password: ')
    updateStash('mint_password', password)

    logger.debug('Asking for mint_mfa_seed')
    seed = getpass('Mint mfa seed (optional): ')
    updateStash('mint_mfa_seed', seed)

    logger.debug('Asking for ynab_api_key')
    api_key = input('YNAB API key: ')
    updateStash('ynab_api_key', api_key.strip())
    logger.debug('Initializing YNAB api.')
    ynapi = YNABAPI(stash.ynab_api_key)

    logger.debug('Asking for ynab_budget_id')
    budgets = ynapi.get_budgets()
    budget_id = usersChoice(budgets)['id']
    updateStash('ynab_budget_id', budget_id)

    logger.debug('Asking for ynab_account_id')
    accounts = ynapi.get_accounts(stash.ynab_budget_id)
    acc_id = usersChoice(accounts)['id']
    updateStash('ynab_account_id', acc_id)


if __name__ == "__main__":
    run()
