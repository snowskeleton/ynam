import logging
from getpass import getpass

from .ynab_api import YNABAPI
from .ynam_secrets import stash, updateStash


def safeInput(cap):
    """guarantees int from user input
    """
    logging.debug(f'Querying user for number less than {cap + 1}')
    ans = int(input(f'Enter 0–{cap}: '))
    if ans and ans <= cap:
        logging.debug(f'User entered: {ans}')
        return ans
    else:
        logging.info('Supplied value outside of range.')
        return safeInput(cap)


def usersChoice(items):
    index = 0
    if len(items) == 1:
        print(f"{items[index]['name']}")
        print('Default to only option')
        return items[index]
    else:
        for item in items:
            print(items.index(item), item['name'])
        index = int(safeInput(len(items) - 1))

        print('selected:', items[index]['name'])
        return items[index]


def run():
    logging.debug('Asking for mint_username')
    updateStash('mint_username', input('Mint username: ').strip())
    logging.debug('Asking for mint_password')
    updateStash('mint_password', getpass('Mint password: '))
    logging.debug('Asking for mint_mfa_seed')
    updateStash('mint_mfa_seed', getpass('Mint mfa seed (optional): '))

    logging.debug('Asking for ynab_api_key')
    updateStash('ynab_api_key', input('YNAB API key: ').strip())
    logging.debug('Initializing YNAB api.')
    ynapi = YNABAPI(stash.ynab_api_key)
    logging.debug('Asking for ynab_budget_id')
    updateStash('ynab_budget_id', usersChoice(ynapi.get_budgets())['id'])
    logging.debug('Asking for ynab_account_id')
    updateStash('ynab_account_id', usersChoice(
        ynapi.get_accounts(stash.ynab_budget_id))['id'])


if __name__ == "__main__":
    run()
