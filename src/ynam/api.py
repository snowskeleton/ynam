import requests, json
from .config import valueOf


def postTransaction(transaction):
    """
    Post new transaction to default budget and account
    """
    result = SendRequest.post(
        f'/budgets/{valueOf("budget_id")}/transactions',
        json=transaction.__data__(),
    )

    return decodeResult(result)


def getAccounts():
    """
    Return list of bank accounts/cards linked to default budget
    """
    result = SendRequest.get(f'/budgets/{valueOf("budget_id")}/accounts')

    return decodeResult(result)['accounts']


def getBudgets():
    """
    Return list of budgets
    """
    result = SendRequest.get(url='/budgets')

    return decodeResult(result)['budgets']


def decodeResult(httpResponse) -> dict:
    answer = json.loads(httpResponse.content.decode('utf-8'))
    return answer['data'] if answer['data'] else answer


class SendRequest():
    uri = 'https://api.youneedabudget.com/v1/'
    defaultHeaders = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + valueOf("api_key")
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
