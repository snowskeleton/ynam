import ast
import mintapi
from .utils import recent, stash
from .parser import arg


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
            headless=arg('headless'),
            wait_for_sync=False,
            wait_for_sync_timeout=10,
        )
        with open(arg('cookies'), 'w+') as file:
            file.write(str(bowser._get_cookies()))

        with open(arg('key'), 'w+') as file:
            file.write(str(bowser._get_api_key_header()))
