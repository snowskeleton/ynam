from datetime import datetime as t, timedelta as delta
import mintapi
from .config import valueOf
from .parser import arg


def dispenseMints():
    tries = 0
    while tries < 10:
        try:
            mint = mintapi.Mint(
                valueOf('username'),
                valueOf('password'),
                mfa_method='soft-token',
                mfa_token=valueOf('mfa_seed_token'),
                headless=arg('headless'),
                session_path=arg('session_file'),
                wait_for_sync=False,
                wait_for_sync_timeout=10,
            )
            return _filter(
                [item['fiData'] for item in mint.get_transaction_data()])
        except:
            tries += 1
    print('Failed to connect to Mint. Exiting.')
    import sys
    sys.exit(1)


def _filter(transactions) -> dict:
    ans = []
    for item in transactions:
        itemDate = t.strptime(item['date'], '%Y-%m-%d')
        itemDate = itemDate.strftime('%Y-%m-%d')
        then = (t.today() - delta(days=int(arg('days')))).strftime('%Y-%m-%d')
        if itemDate >= then:
            ans.append(item)
    return ans
