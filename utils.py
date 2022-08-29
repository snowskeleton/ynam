from datetime import datetime, timedelta
import mintapi
import json


def allTransactions():
    mint = mintapi.Mint(
        Secrets.username(),
        Secrets.password(),

        headless=True,
        session_path='/Users/snow/.mintapi/session',
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


class Secrets():
    with open('secrets.json') as f:
        secrets = json.load(f)

    @classmethod
    def budget_id(self):
        return self.secrets['budget_id']

    @classmethod
    def api_key(self):
        return self.secrets['api_key']

    @classmethod
    def username(self):
        return self.secrets['username']

    @classmethod
    def password(self):
        return self.secrets['password']

    @classmethod
    def account_id(self):
        return self.secrets['account_id']


class YNABTransaction():
    def __init__(self, transaction):
        self.id = transaction["id"]
        self.cleared = False
        self.approved = False
        self.flag_color = None
        self.account_id = Secrets.account_id()
        self.date = transaction['date']
        self.amount = int(transaction['amount'] * 1000)
        self.payee_name = transaction['description']

    def __dict__(self):
        return {
            "transaction": {
                "date": f"{self.date}",
                "amount": self.amount,
                "account_id": f"{self.account_id}",
                "payee_name": f"{self.payee_name}",
            }
        }
