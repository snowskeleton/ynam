from getpass import getpass

from .ynab_api import YNABAPI
from .ynam_secrets import stash, updateStash


def safeInput(cap):
    """guarantees int from user input
    """
    while True:
        ans = input(f'Enter 0–{cap}: ')

        try:
            if int(ans) <= cap:
                return int(ans)
        except:
            # failed to convert user input to integer. start over
            continue


def usersChoice(items):
    index = 0
    if len(items) == 1:
        print(f"{items[0]['name']}")
        print('Default to only option')
        return items[index]
    else:
        for item in items:
            print(items.index(item), item['name'])
        index = int(safeInput(len(items) - 1))

        print('selected:', items[index]['name'])
        return items[index]


def run():
    updateStash('mint_username', input('Mint username: ').strip())
    updateStash('mint_password', getpass('Mint password: '))
    updateStash('mint_mfa_seed', getpass('Mint mfa seed (optional): '))

    updateStash('ynab_api_key', input('YNAB API key: ').strip())
    ynapi = YNABAPI(stash.ynab_api_key)
    updateStash('ynab_budget_id', usersChoice(ynapi.get_budgets())['id'])
    updateStash('ynab_account_id', usersChoice(ynapi.get_accounts())['id'])


if __name__ == "__main__":
    run()
