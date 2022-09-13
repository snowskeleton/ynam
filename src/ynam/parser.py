import argparse
import os
from ._version import __version__

parser = argparse.ArgumentParser(description='You Need a Mint (YNAM)')
add = parser.add_argument

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
    default=os.path.expanduser('~/.ynamrc'),
    help='Custom ynam config file path')
add('--session-file',
    '-s',
    dest='session_file',
    action='store',
    default=os.path.expanduser('~/.mintapi/session'),
    help='Custom file path to chromium session')
add('--chromedriver-file',
    '-C',
    dest='chromdriver',
    action='store',
    default=os.path.expanduser('~/.mintapi/chromedriver'),
    help='Custom file path to chromiumdriver')

args = parser.parse_args()


def arg(key):
    return vars(args)[key]
