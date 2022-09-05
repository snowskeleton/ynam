import argparse


def parse():
    p = argparse.ArgumentParser(description='You Need a Mint (YNAM)')
    p.add_argument('-v, --version',
                   action='version',
                   version='snowskeleton/ynam v0.1.1')
    p.add_argument('-q, --quickstart',
                   dest='q',
                   action='store_true',
                   help='A required integer positional argument')
    args = p.parse_args()
    if args.q:
        from .quickstart import run
        run()
