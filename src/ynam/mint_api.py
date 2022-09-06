from datetime import datetime as t, timedelta as delta
import mintapi
from .config import valueOf
from .parser import arg


def dispenseMints():
    mint = mintapi.Mint(
        valueOf('username'),
        valueOf('password'),
        headless=arg('headless'),
        session_path=arg('mint_session_file'),
        wait_for_sync=True,
        wait_for_sync_timeout=300,
    )
    return _filter([item['fiData'] for item in mint.get_transaction_data()])


def _filter(transactions) -> dict:
    ans = []
    for item in transactions:
        itemDate = t.strptime(item['date'], '%Y-%m-%d')
        itemDate = itemDate.strftime('%Y-%m-%d')
        then = (t.today() - delta(days=int(arg('days')))).strftime('%Y-%m-%d')
        if itemDate >= then:
            ans.append(item)
    return ans
