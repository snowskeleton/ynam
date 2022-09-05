from datetime import datetime, timedelta
import requests
import os
import mintapi
from config import valueOf


def allTransactions():
    mint = mintapi.Mint(
        valueOf('username'),
        valueOf('password'),
        headless=True,
        session_path=os.path.expanduser('~') + '/.mintapi/session',
        wait_for_sync=True,
        wait_for_sync_timeout=300,
    )
    return yesterdaysTransactions(
        [item['fiData'] for item in mint.get_transaction_data()]
    )


def yesterdaysTransactions(transactions) -> dict:
    ans = []
    for item in transactions:
        itemDate = datetime.strptime(item['date'], '%Y-%m-%d')
        itemDate = itemDate.strftime('%Y-%m-%d')
        earlier = (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
        if itemDate > earlier:
            ans.append(item)
    return ans


class YNABTransaction():
    def __init__(self, transaction):
        self.account_id = valueOf('account_id')
        self.date = transaction['date']
        self.amount = int(transaction['amount'] * 1000)
        self.payee_name = transaction['description']

    def __data__(self):
        return {
            "transaction": {
                "date": self.date,
                "amount": self.amount,
                "account_id": self.account_id,
                "payee_name": self.payee_name,
            }
        }


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
