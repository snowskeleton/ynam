import argparse
from datetime import datetime as t
from datetime import timedelta as delta
from pathlib import Path, PurePath

from ._version import __version__


def path(path):
    return PurePath.joinpath(Path.home(), path)


parser = argparse.ArgumentParser(description='You Need a Mint (YNAM)')
add = parser.add_argument

add('--account-id',
    dest='ynab_account_id',
    action='store',
    default=None,
    help='YNAB account ID')
add('--blab',
    dest='blab',
    action='store_true',
    help='Print config info and exit')
add('--budget-id',
    dest='ynab_budget_id',
    action='store',
    default=None,
    help='YNAB budget ID')
add('--chromedriver-file',
    '-C',
    dest='chromdriver',
    action='store',
    default=path('.ynam_chromedriver'),
    type=argparse.FileType('r+'),
    help='Custom file path to chromiumdriver')
add('--config-file-path',
    '-c',
    dest='config_file_path',
    action='store',
    default=path('.ynamrc'),
    type=argparse.FileType('r+'),
    help='Custom ynam config file path')
add('--cookies',
    dest='mint_cookies',
    action='store',
    default=path('.ynam_mintapi_cookies'),
    type=argparse.FileType('r+'),
    help='Custom file path to session cookies')
add('--days',
    '-d',
    dest='days',
    action='store',
    type=lambda d: (t.today() - delta(days=int(d))).strftime("%y-%m-%d"),
    default='1',
    help='Cutoff (in days) for how far back to search'
    'A value of 0 gets transactions from today only')
add('--deviate',
    dest='deviate',
    action='store_true',
    help='Do developer-y things')
add('--dryrun',
    '-D',
    dest='dryrun',
    action='store_true',
    help='Print transactions instead of posting to YNAB')
add('--graphics',
    '-x',
    '-g',
    dest='headless',
    action='store_false',
    help='Flag to run non-headless. Used to input 2FA codes')
add('--mfa-seed',
    dest='mint_mfa_seed',
    action='store',
    default=None,
    help='Mint MFA token seed')
add('--mint-api-key-file',
    dest='mint_api_key_file',
    action='store',
    default=path('.ynam_mintapi_api_key'),
    type=argparse.FileType('r+'),
    help='Custom file path to api key')
add('--password',
    dest='mint_password',
    action='store',
    default=None,
    help='Mint password')
add('--print-ynab-transactions',
    dest='print_ynab_transactions',
    action='store_true',
    help='Print ynab transactions and exit')
add('--quickstart',
    '-q',
    dest='quickstart',
    action='store_true',
    help='A required integer positional argument')
add('--session-file',
    '-s',
    dest='session_file',
    action='store',
    default=path('.ynam_mintapi_session'),
    type=argparse.FileType('r+'),
    help='Custom file path to chromium session')
add('--username',
    dest='mint_username',
    action='store',
    default=None,
    help='Mint username')
add('--update-mint-auth',
    dest='update_auth',
    action='store_true',
    help='Grab new api_key and cookies from Selinum session, then exit')
add('--use-chromedriver-on-path',
    action='store_true',
    help=
    'Whether to use the chromedriver on PATH, instead of downloading a local copy.'
    )
add('--verbose', action='store_true', help='Enables console output')
add('--version',
    '-v',
    action='version',
    version='snowskeleton/ynam ' + __version__)
add('--ynab-api-key-literal',
    dest='ynab_api_key',
    action='store',
    type=str,
    default=None,
    help='Literal string api key')

args = parser.parse_args()


def arg(key):
    return vars(args)[key]
