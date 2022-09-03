from getpass import getpass
from config import update, secretsPath
from api import getBudgets, getAccounts


def usersChoice(items):
  index = 0
  if len(items) == 1:
    print('Default to only option')
  else:
    for item in items:
      print(items.index(item), item['name'])
    index = int(input(f'Enter 0–{len(items) - 1}: '))

    print('selected: ', items[index]['name'])
    return items[index]


def run():
  update('api_key', input('API key: '))
  update('username', input('Mint username: '))
  update('password', getpass('Mint password: '))
  update('budget_id', usersChoice(getBudgets())['id'])
  update('account_id', usersChoice(getAccounts())['id'])


if __name__ == "__main__":
  run()
