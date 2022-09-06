from datetime import datetime, timedelta
import mintapi
from .config import valueOf
from .parser import arg


def getTransactions():
    mint = mintapi.Mint(
        valueOf('username'),
        valueOf('password'),
        headless=arg('headless'),
        session_path=arg('mint_session_file'),
        wait_for_sync=True,
        wait_for_sync_timeout=300,
    )
    return yesterdaysTransactions(
        [item['fiData'] for item in mint.get_transaction_data()])


def yesterdaysTransactions(transactions) -> dict:
    ans = []
    for item in transactions:
        itemDate = datetime.strptime(item['date'], '%Y-%m-%d')
        itemDate = itemDate.strftime('%Y-%m-%d')
        earlier = (datetime.today() -
                   timedelta(days=int(arg('days')))).strftime('%Y-%m-%d')
        if itemDate >= earlier:
            ans.append(item)
    return ans

