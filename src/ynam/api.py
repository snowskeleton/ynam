from utils import SendRequest
from config import valueOf
import json


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
