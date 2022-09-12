import argparse
import os
from ._version import __version__

parser = argparse.ArgumentParser(description='You Need a Mint (YNAM)')
add = parser.add_argument

add('-v, --version',
    action='version',
    version='snowskeleton/ynam ' + __version__)
add('-q',
    '--quickstart',
    dest='quickstart',
    action='store_true',
    help='A required integer positional argument')
add('-x',
    '-g',
    '--graphics',
    dest='headless',
    action='store_false',
    help='Flag to run non-headless. Used to input 2FA codes')
add('-d',
    '--days',
    dest='days',
    action='store',
    default='1',
    help='Cutoff (in days) for how far back to search'
    'A value of 0 gets transactions from today only')
add('--dryrun',
    dest='dryrun',
    action='store_true',
    help='Print transactions instead of posting to YNAB')
add('--config',
    dest='config_file_path',
    action='store',
    default=os.path.expanduser('~/.ynamrc'),
    help='Custom ynam config file path')
add('--mint-session-file',
    dest='mint_session_file',
    action='store',
    default=os.path.expanduser('~/.mintapi/session'),
    help='Custom mint session file path')

args = parser.parse_args()


def arg(key):
    return vars(args)[key]
