# flake8: noqa
import argparse
import sys

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('--configuration')
args, sys.argv = parser.parse_known_args(sys.argv)
if args.configuration == 'Production':
    from .production import Production
else:
    from .local import Local
