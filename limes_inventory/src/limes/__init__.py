# from . import limes
import sys

from limes_common import coms

def main(args=None):
    if args is None:
        args = sys.argv[1:]

    for a in args:
        print(a)

print(__file__)