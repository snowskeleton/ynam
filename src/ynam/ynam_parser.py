import argparse
import logging
from datetime import datetime as t
from datetime import timedelta as delta
from pathlib import Path, PurePath

from ._version import __version__


def migrate_v0_3_4_0():
    import os
    import shutil

    def path(path):
        return PurePath.joinpath(Path.home(), path)
    old_file_paths = [
        (path('.ynam_chromedriver'), CHROMEDRIVER),
        (path('.ynam_mintapi_api_key'), API_KEY),
        (path('.ynam_mintapi_cookies'), COOKIES),
        (path('.ynam_mintapi_session'), SESSION),
        (path('.ynamrc'), SECRETS_FILE),
    ]
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    for file in old_file_paths:
        if os.path.exists(file[0]):
            shutil.move(file[0], file[1])


basedir = PurePath.joinpath(Path.home(), '.ynam/')
CHROMEDRIVER = basedir / 'chromedriver'
SECRETS_FILE = basedir / 'secrets.json'
COOKIES = basedir / 'selenium_cookies'
SESSION = basedir / 'selenium_session'
API_KEY = basedir / 'mint_api_key'


parser = argparse.ArgumentParser(description='You Need a Mint (YNAM)')
add = parser.add_argument

# YNAB info
add('--account-id',
    dest='ynab_account_id',
    action='store',
    default=None,
    help='YNAB account ID')
add('--budget-id',
    dest='ynab_budget_id',
    action='store',
    default=None,
    help='YNAB budget ID')
add('--ynab-api-key-literal',
    dest='ynab_api_key',
    action='store',
    type=str,
    default=None,
    help='Literal string api key')

# Mint info
# required
add('--username',
    dest='mint_username',
    action='store',
    default=None,
    help='Mint username')
add('--password',
    dest='mint_password',
    action='store',
    default=None,
    help='Mint password')
add('--mfa-seed',
    dest='mint_mfa_seed',
    action='store',
    default=None,
    help='Mint MFA token seed')

# optional
add('--cookies',
    dest='mint_cookies',
    action='store',
    default=COOKIES,
    type=argparse.FileType('r+'),
    help='Custom file path to session cookies')
add('--mint-api-key-file',
    dest='mint_api_key_file',
    action='store',
    default=API_KEY,
    type=argparse.FileType('r+'),
    help='Custom file path to api key')
add('--session-file',
    '-s',
    dest='session_file',
    action='store',
    default=SESSION,
    type=argparse.FileType('r+'),
    help='Custom file path to chromium session')

# mintapi - Selenium
add('--chromedriver-file',
    '-C',
    dest='chromedriver',
    action='store',
    default=CHROMEDRIVER,
    type=argparse.FileType('r+'),
    help='Custom file path to chromiumdriver')
add('--use-chromedriver-on-path',
    action='store_true',
    help='Use the chromedriver on PATH, instead of newly downloaded copy.')

# General
add('--days',
    '-d',
    dest='days',
    action='store',
    type=lambda d: (t.today() - delta(days=int(d))).strftime("%Y-%m-%d"),
    default='10',
    help='Cutoff (in days) for how far back to search'
    'A value of 0 gets transactions from today only')
add('--graphics',
    '-x',
    '-g',
    dest='headless',
    action='store_false',
    help='Flag to run non-headless. Used to input 2FA codes')
add('--secrets-file',
    '-c',
    dest='secrets_file',
    action='store',
    default=SECRETS_FILE,
    type=argparse.FileType('r+'),
    help='Custom ynam config file path')

# Special cases
add('--print-ynab-transactions',
    dest='print_ynab_transactions',
    action='store_true',
    help='Print ynab transactions and exit')
add('--dryrun',
    '-D',
    dest='dryrun',
    action='store_true',
    help='Print transactions instead of posting to YNAB')
add('--quickstart',
    '-q',
    dest='quickstart',
    action='store_true',
    help='Enter credentials and select default budget/card')
add('--update-mint-auth',
    dest='update_auth',
    action='store_true',
    help='Grab new api_key and cookies from Selinum session, then exit')
add('--blab',
    dest='blab',
    action='store_true',
    help='Print config info and exit')
add('--deviate',
    dest='deviate',
    action='store_true',
    help='Do developer-y things')
add('--version',
    '-v',
    action='version',
    version='snowskeleton/ynam ' + __version__)

# Logging
add('--debug',
    help="Print lots of debugging statements",
    action="store_const",
    dest="loglevel",
    const=logging.DEBUG,
    default=logging.WARNING,)
add('--verbose',
    help="Enable console output",
    action="store_const",
    dest="loglevel",
    const=logging.INFO,)

args = parser.parse_args()

logging.basicConfig(level=args.loglevel)
handle = 'ynam'
logger = logging.getLogger(handle)


def arg(key):
    logger.debug(f'Fetch for key: {key}')
    val = vars(args)[key]
    logger.debug(f'Fetched vaule: {val}')
    return val
