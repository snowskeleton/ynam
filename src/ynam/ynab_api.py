import requests, json
from .utils import recent, stash


def postTransaction(budgetID, transaction):
    """
    Post new transaction to default budget and account
    """
    # nt['import_id'] = f"YNAM:{nt['amount']}:{time.time()}"
    results = SendRequest.post(
        f'/budgets/{budgetID}/transactions',
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


def getTransactions(budgetID, since_date, type):
    result = SendRequest.get(
        f'/budgets/{budgetID}/transactions',
        json={"data": {
            "since_date": since_date,
            "type": type,
        }},
    )

    return recent(_decoded(result)['transactions'])


def getAccounts(budgetID):
    """
    Return list of bank accounts/cards linked to default budget
    """
    result = SendRequest.get(f'/budgets/{budgetID}/accounts')

    return _decoded(result)['accounts']


def getBudgets():
    """
    Return list of budgets
    """
    result = SendRequest.get(url='/budgets')

    return _decoded(result)['budgets']


def _decoded(httpResponse) -> dict:
    answer = json.loads(httpResponse.content.decode('utf-8'))
    return answer['data'] if answer['data'] else answer


class SendRequest():
    uri = 'https://api.youneedabudget.com/v1/'
    defaultHeaders = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + stash.valueOf("api_key")
    }

    @classmethod
    def post(self, url, **kwargs):
        return requests.post(self.uri + url,
                             headers=self.defaultHeaders,
                             **kwargs)

    @classmethod
    def get(self, url, **kwargs):
        return requests.get(self.uri + url,
                            headers=self.defaultHeaders,
                            **kwargs)
