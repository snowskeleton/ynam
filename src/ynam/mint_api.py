import mintapi
from .utils import recent
from .quickstart import updateAuth


def dispenseMints(cookies, key):
    try:
        mints = mintapi.RESTClient()
        mints.authorize(cookies, key)
        return recent(
            [item['fiData'] for item in mints.get_transaction_data()])
    except:
        updateAuth()
        # mints = mintapi.RESTClient()
        mints.authorize(cookies, key)
        return recent(
            [item['fiData'] for item in mints.get_transaction_data()])


def browser():
    return mintapi.SeleniumBrowser()
