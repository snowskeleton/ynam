import ast
import mintapi
from .utils import stash
from .parser import arg

import sys
import requests, json
from datetime import datetime as t, timedelta as delta


class MintAPI():

    def __init__(self) -> None:
        self.restClient = mintapi.RESTClient
        self.browser = mintapi.SeleniumBrowser
        self.cpath = arg('cookies')
        self.keypath = arg('key')

    def dispenseMints(self):
        client = self.restClient()
        key = self.key()
        cookies = self.cookies()

        client.authorize(cookies, key)
        try:
            items = client.get_transaction_data()
        except:
            self.updateAuth()
            client.authorize(cookies, key)
            items = client.get_transaction_data()
        finally:
            return recent([item['fiData'] for item in items])

    def cookies(self):
        try:
            with open(self.cpath, 'r') as file:
                return ast.literal_eval(file.read())
        except FileNotFoundError:
            self.updateAuth()
            with open(self.cpath, 'r') as file:
                return ast.literal_eval(file.read())

    def key(self):
        try:
            with open(self.keypath, 'r') as file:
                return ast.literal_eval(file.read())['authorization']
        except FileNotFoundError:
            self.updateAuth()
            with open(self.keypath, 'r') as file:
                return ast.literal_eval(file.read())['authorization']

    def updateAuth(self):
        bowser = self.browser(
            email=stash.valueOf('username'),
            password=stash.valueOf('password'),
            mfa_method='soft-token',
            mfa_token=stash.valueOf('mfa_seed_token'),
            use_chromedriver_on_path=arg('use_chromedriver_on_path'),
            headless=arg('headless'),
            wait_for_sync=False,
            wait_for_sync_timeout=10,
        )
        with open(arg('cookies'), 'w+') as file:
            file.write(str(bowser._get_cookies()))

        with open(arg('key'), 'w+') as file:
            file.write(str(bowser._get_api_key_header()))

    @classmethod
    def asYNAB(transaction: dict):
        nt = {}
        nt['date'] = transaction['date']
        nt['amount'] = int(transaction['amount'] * 1000)
        nt['account_id'] = stash.valueOf('account_id')
        nt['payee_name'] = transaction['inferredDescription']
        nt['import_id'] = transaction['id']
        nt['cleared'] = "cleared"
        return nt


class YNABAPI():

    def __init__(self) -> None:
        self.uri = 'https://api.youneedabudget.com/v1/'
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {stash.valueOf("api_key")}'
        }

    def _post(self, url, **kwargs):
        return requests.post(self.uri + url, **kwargs, headers=self.headers)

    def _get(self, url, **kwargs):
        return requests.get(self.uri + url, **kwargs, headers=self.headers)

    def bulkPostTransactions(self, transactions: dict):
        results = self._post(
            f'/budgets/{stash.valueOf("budget_id")}/transactions',
            json={"transactions": transactions},
        )

        return _decoded(results)

    def postTransaction(self, transaction):
        """
        Post new transaction to default budget and account
        """
        results = self._post(
            self.uri + f'/budgets/{stash.valueOf("budget_id")}/transactions',
            json={
                "transaction": {
                    "date": transaction['date'],
                    "amount": int(transaction['amount']),
                    "account_id": transaction['account_id'],
                    "payee_name": transaction['payee_name'],
                    "import_id": transaction['import_id'],
                    "cleared": "cleared",
                }
            },
        )

        return _decoded(results)

    def getTransactions(self, since_date: str = '', type: str = ''):
        """
        Return all recent transactions
        """
        result = self._get(
            f'/budgets/{stash.valueOf("budget_id")}/transactions',
            json={"data": {
                "since_date": since_date,
                "type": type,
            }},
        )

        return recent(_decoded(result)['transactions'])

    def getAccounts(self):
        """
        Return list of bank accounts/cards linked to default budget
        """
        result = self._get(f'/budgets/{stash.valueOf("budget_id")}/accounts')

        return _decoded(result)['accounts']

    def getBudgets(self):
        """
        Return list of budgets
        """
        result = self._get(url='/budgets')

        return _decoded(result)['budgets']


def recent(transactions) -> dict:
    ans = []
    for item in transactions:
        itemDate = t.strptime(item['date'], '%Y-%m-%d')
        if dateCalc(itemDate.strftime('%Y-%m-%d')):
            ans.append(item)
    return ans


def dateCalc(date):
    return date >= (t.today() -
                    delta(days=int(arg('days')))).strftime('%Y-%m-%d')


def _decoded(httpResponse) -> dict:
    answer = json.loads(httpResponse.content.decode('utf-8'))
    try:
        return answer['data'] if answer['data'] else answer
    except Exception as e:
        print(answer)
        print(e)
        sys.exit()
