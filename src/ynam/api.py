from dataclasses import dataclass, asdict
import ast
import inspect
import requests, json
import mintapi
from .secrets import stash
from .parser import arg

tfmt = '%Y-%m-%d'


@dataclass
class MintTransaction:

    date: str
    amount: int
    inferredDescription: str
    id: str

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v
            for k, v in env.items() if k in inspect.signature(cls).parameters
        })

    def asDict(self):
        return asdict(self)

    def asYNAB(self):
        return YNABTransaction(
            **{
                "date": self.date,
                "amount": int(self.amount * 1000),
                "account_id": stash.ynab_account_id,
                "payee_name": self.inferredDescription,
                "import_id": self.id,
            })


@dataclass
class YNABTransaction:

    date: str
    amount: int
    account_id: str
    payee_name: str
    import_id: str
    id: str = None
    payee_id: str = None
    category_id: str = None
    memo: str = None
    cleared: str = None
    approved: str = None
    flag_color: str = None
    subtransactions: list = None
    cleared: str = 'cleared'

    def __post_init__(self):
        self.payee_name = self.payee_name[:100]

    def asDict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, env):
        return cls(**{
            k: v
            for k, v in env.items() if k in inspect.signature(cls).parameters
        })


class MintAPI():

    def __init__(self) -> None:
        self.restClient = mintapi.RESTClient
        self.browser = mintapi.SeleniumBrowser
        self.cpath = arg('mint_cookies')
        self.keypath = arg('mint_api_key_file')

    def getXtns(self):
        client = self.restClient()
        try:
            client.authorize(self.cookies(), self.key())
        except IsADirectoryError as e:
            print(e)
            print("""
                  One or more expected files is a directory instead \n
                  If you don't have a value to supply, simply create \n
                  an empty file in the desired location \n
                  """)
        except Exception as e:
            self.updateAuth()
            client.authorize(self.cookies(), self.key())
        finally:
            items = client.get_transaction_data()
            return [
                MintTransaction.from_dict(item['fiData']) for item in items
            ]

    def cookies(self):
        with open(self.cpath, 'r') as file:
            return ast.literal_eval(file.read())

    def key(self):
        with open(self.keypath, 'r') as file:
            return ast.literal_eval(file.read())['authorization']

    def updateAuth(self):
        bowser = self.browser(
            email=stash.mint_username,
            password=stash.mint_password,
            mfa_method='soft-token',
            mfa_token=stash.mint_mfa_seed,
            use_chromedriver_on_path=arg('use_chromedriver_on_path'),
            headless=arg('headless'),
            wait_for_sync=False,
            wait_for_sync_timeout=10,
        )
        with open(arg('mint_cookies'), 'w+') as file:
            file.write(str(bowser._get_cookies()))

        with open(arg('mint_api_key_file'), 'w+') as file:
            file.write(str(bowser._get_api_key_header()))


class YNABAPI():

    def __init__(self) -> None:
        self.uri = 'https://api.youneedabudget.com/v1/'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {stash.ynab_api_key}"
        }

    def _patch(self, url, **kwargs):
        return requests.patch(self.uri + url, **kwargs, headers=self.headers)

    def _post(self, url, **kwargs):
        return requests.post(self.uri + url, **kwargs, headers=self.headers)

    def _get(self, url, **kwargs):
        return requests.get(self.uri + url, **kwargs, headers=self.headers)

    def bulkPatchTransactions(self, transactions: list):
        url = f'/budgets/{stash.ynab_budget_id}/transactions'
        # this json doesn't seem to like being too long. it works
        # with 10 items, and breaks with 250, but I'm not sure where
        # they meet
        json = {"transactions": transactions}
        results = self._patch(
            url,
            json=json,
        )

        return real(results)

    def bulkPostTransactions(self, transactions: list):
        results = self._post(
            f'/budgets/{stash.ynab_budget_id}/transactions',
            json={"transactions": transactions},
        )

        return real(results)

    def getUglyTransactions(self, since_date: str = '', type: str = ''):
        """
        Return transactions as raw json
        """
        return self._get(
            f'/budgets/{stash.ynab_budget_id}/transactions',
            json={"data": {
                "since_date": since_date,
                "type": type,
            }},
        )

    def getXtns(self, since_date: str = '', type: str = ''):
        """
        Return transactions as YNABTransaction dataclass objects
        """
        result = self.getUglyTransactions(since_date, type)
        return [
            YNABTransaction.from_dict(xt)
            for xt in real(result)['transactions']
        ]

    def printXtns(self, since_date: str = '', type: str = ''):
        result = self.getUglyTransactions(since_date, type)
        print(
            json.dumps(([xt for xt in real(result)['transactions']]),
                       indent=2))

    def getAccounts(self):
        """
        Return list of bank accounts/cards linked to default budget
        """
        return real(
            self._get(f'/budgets/{stash.ynab_budget_id}/accounts'))['accounts']

    def getBudgets(self):
        """
        Return list of budgets
        """
        return real(self._get(url='/budgets'))['budgets']


def real(httpResponse) -> dict:
    answer = json.loads(httpResponse.content.decode('utf-8'))
    try:
        return answer['data']
    except KeyError:
        print(answer['error'])
