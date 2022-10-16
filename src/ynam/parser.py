import argparse
import posixpath
from ._version import __version__

parser = argparse.ArgumentParser(description='You Need a Mint (YNAM)')
add = parser.add_argument


def safePath(*args):
    path = posixpath.join(*args)
    return posixpath.expanduser(path)


add('--version',
    '-v',
    action='version',
    version='snowskeleton/ynam ' + __version__)
add('--quickstart',
    '-q',
    dest='quickstart',
    action='store_true',
    help='A required integer positional argument')
add('--graphics',
    '-x',
    '-g',
    dest='headless',
    action='store_false',
    help='Flag to run non-headless. Used to input 2FA codes')
add('--days',
    '-d',
    dest='days',
    action='store',
    default='1',
    help='Cutoff (in days) for how far back to search'
    'A value of 0 gets transactions from today only')
add('--dryrun',
    '-D',
    dest='dryrun',
    action='store_true',
    help='Print transactions instead of posting to YNAB')
add('--config-file-path',
    '-c',
    dest='config_file_path',
    action='store',
    default=safePath('~', '.ynamrc'),
    help='Custom ynam config file path')
add('--session-file',
    '-s',
    dest='session_file',
    action='store',
    default=safePath('~', '.mintapi_session'),
    help='Custom file path to chromium session')
add('--chromedriver-file',
    '-C',
    dest='chromdriver',
    action='store',
    default=safePath('~', '.mintapi_chromedriver'),
    help='Custom file path to chromiumdriver')
add('--cookies',
    dest='cookies',
    action='store',
    default=safePath('~', '.mintapi_cookies'),
    help='Custom file path to session cookies')
add('--api-key',
    dest='key',
    action='store',
    default=safePath('~', '.mintapi_api_key'),
    help='Custom file path to api key')
add('--blab',
    dest='blab',
    action='store_true',
    help='Print config info and exit')
add('--deviate',
    dest='deviate',
    action='store_true',
    help='Do developer-y things')
add('--update-mint-auth',
    dest='update_auth',
    action='store_true',
    help='Grab new api_key and cookies from Selinum session, then exit')
add('--use-chromedriver-on-path',
    action='store_true',
    help='Whether to use the chromedriver on PATH, \
        instead of downloading a local copy.')

args = parser.parse_args()


def arg(key):
    return vars(args)[key]
