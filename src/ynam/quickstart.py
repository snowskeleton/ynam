from getpass import getpass
from .config import update, newfile


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
    newfile()

    update('username', input('Mint username: ').strip())
    update('password', getpass('Mint password: '))
    update('mfa_seed_token', getpass('Mint mfa seed (optional): '))

    # import from ynab_api fails unless we have api_key
    update('api_key', input('YNAB API key: ').strip())
    from .ynab_api import getBudgets, getAccounts
    update('budget_id', usersChoice(getBudgets())['id'])
    update('account_id', usersChoice(getAccounts())['id'])


if __name__ == "__main__":
    run()
