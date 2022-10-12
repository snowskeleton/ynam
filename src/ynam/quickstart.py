from getpass import getpass
from .utils import stash
from .parser import arg as cliArg


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
    stash.newfile()

    stash.update('username', input('Mint username: ').strip())
    stash.update('password', getpass('Mint password: '))
    stash.update('mfa_seed_token', getpass('Mint mfa seed (optional): '))

    # import from ynab_api fails unless we have api_key
    stash.update('api_key', input('YNAB API key: ').strip())
    from .ynab_api import getBudgets, getAccounts
    stash.update('budget_id', usersChoice(getBudgets())['id'])
    stash.update('account_id', usersChoice(getAccounts())['id'])


def updateAuth():
    from mintapi import SeleniumBrowser
    mints = SeleniumBrowser(
        email=stash.valueOf('username'),
        password=stash.valueOf('password'),
        mfa_method='soft-token',
        mfa_token=stash.valueOf('mfa_seed_token'),
        headless=cliArg('headless'),
        session_path=cliArg('session_file'),
        wait_for_sync=False,
        wait_for_sync_timeout=10,
    )
    with open(cliArg('cookies'), 'w+') as file:
        file.write(str(mints._get_cookies()))

    with open(cliArg('key'), 'w+') as file:
        file.write(str(mints._get_api_key_header()))

if __name__ == "__main__":
    run()
