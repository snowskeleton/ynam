from getpass import getpass
from .secrets import updateStash
from .api import YNABAPI


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
    updateStash('username', input('Mint username: ').strip())
    updateStash('password', getpass('Mint password: '))
    updateStash('mfa_seed_token', getpass('Mint mfa seed (optional): '))

    updateStash('api_key', input('YNAB API key: ').strip())
    ynapi = YNABAPI()
    updateStash('budget_id', usersChoice(ynapi.getBudgets())['id'])
    updateStash('account_id', usersChoice(ynapi.getAccounts())['id'])


if __name__ == "__main__":
    run()
