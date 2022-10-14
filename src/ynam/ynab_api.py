import sys
import requests, json
from .utils import recent, stash


def _decoded(httpResponse) -> dict:
    answer = json.loads(httpResponse.content.decode('utf-8'))
    try:
        return answer['data'] if answer['data'] else answer
    except Exception as e:
        print(answer)
        print(e)
        sys.exit()


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
