from datetime import datetime as t, timedelta as delta
from .easyConfig import Configer
from .parser import arg


class Secrets(Configer):

    def __init__(self, name):
        super().__init__(name)


stash = Secrets('ynamrc')


def recent(transactions) -> dict:
    ans = []
    for item in transactions:
        itemDate = t.strptime(item['date'], '%Y-%m-%d')
        if dateCalc(itemDate.strftime('%Y-%m-%d')):
            ans.append(item)
    return ans


def dateCalc(date):
    return date >= (t.today() -
                    delta(days=int(arg('days')))).strftime('%Y-%m-%d')


def mintToYnab(transaction: dict):
    nt = {}
    nt['date'] = transaction['date']
    nt['amount'] = int(transaction['amount'] * 1000)
    nt['account_id'] = stash.valueOf('account_id')
    nt['payee_name'] = transaction['inferredDescription']
    nt['import_id'] = transaction['id']
    nt['cleared'] = "cleared"
    return nt
