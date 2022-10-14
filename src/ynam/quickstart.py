from getpass import getpass
from .utils import stash
from .ynab_api import YNABAPI


def safeInput(cap):
    """ guarantees int from user input
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
        print('Default to only option')
    else:
        for item in items:
            print(items.index(item), item['name'])
        index = int(safeInput(len(items) - 1))

        print('selected:', items[index]['name'])
        return items[index]


def run():
    for key in [
            'api_key',
            'username',
            'password',
            'account_id',
            'budget_id',
            'mfa_seed_token',
    ]:
        stash.update(key, '')
    stash.update('username', input('Mint username: ').strip())
    stash.update('password', getpass('Mint password: '))
    stash.update('mfa_seed_token', getpass('Mint mfa seed (optional): '))

    stash.update('api_key', input('YNAB API key: ').strip())
    ynapi = YNABAPI()
    stash.update('budget_id', usersChoice(ynapi.getBudgets())['id'])
    stash.update('account_id', usersChoice(ynapi.getAccounts())['id'])


if __name__ == "__main__":
    run()
