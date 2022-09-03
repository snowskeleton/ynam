import requests
from config import valueOf
import json

uri = 'https://api.youneedabudget.com/v1/'
defaultHeaders = {'Content-Type': 'application/json',
                  'Authorization': f'Bearer {valueOf("api_key")}'}


def postTransaction(transaction):
  """
  Post new transaction to default budget and account
  """
  result = requests.post(
      f'{uri}/budgets/{valueOf("budget_id")}/transactions',
      json=transaction.__data__(),
      headers=defaultHeaders,
  )

  return decodeResult(result)


def getAccounts():
  """
  Return list of bank accounts/cards linked to default budget
  """
  result = requests.get(
      f'{uri}/budgets/{valueOf("budget_id")}/accounts', headers=defaultHeaders)

  return decodeResult(result)['accounts']


def getBudgets():
  """
  Return list of budgets
  """

  result = requests.get(f'{uri}/budgets', headers=defaultHeaders)

  return decodeResult(result)['budgets']


def decodeResult(httpResponse: requests.models.Response) -> dict:
  answer = json.loads(httpResponse.content.decode('utf-8'))
  return answer['data'] if answer['data'] else answer
