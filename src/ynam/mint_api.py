import ast
import inspect
from dataclasses import dataclass

import mintapi

from .ynam_parser import arg
from .ynam_secrets import stash
from .ynab_api import YNABTransaction


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

    def asYNAB(self):
        return YNABTransaction(
            **{
                "date": self.date,
                "amount": int(self.amount * 1000),
                "account_id": stash.ynab_account_id,
                "payee_name": self.inferredDescription,
                "import_id": self.id,
            })


class MintAPI():

    def __init__(self) -> None:
        self.restClient = mintapi.RESTClient
        self.browser = mintapi.SeleniumBrowser
        self.cpath = arg('mint_cookies')
        self.keypath = arg('mint_api_key_file')

    def getXtns(self, start_date: str = None):
        try:
            client = self.restClient()
            client.authorize(self.cookies(), self.key())
            items = client.get_transaction_data()
            items = [
                MintTransaction.from_dict(item['fiData']) for item in items
            ]
            items = [item for item in items if item.date > start_date]
            return items
        except IsADirectoryError as e:
            print(e)
            print("""
                  One or more expected files is a directory instead \n
                  If you don't have a value to supply, simply create \n
                  an empty file in the desired location \n
                  """)

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
