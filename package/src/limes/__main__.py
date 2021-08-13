from . import limes

import sys
from typing import List
from getpass import getpass
from functools import reduce

from .tools.qol import Switch, T
from .res import strings as Constants
from limes_common import config

def main(args:List[str] = sys.argv[1:]):
    # for later abstraction of help
    class Command:
        def __init__(self, schemas, options) -> None:
            self.schemas = schemas
            self.options = options

        def printHelp(self):
            self.printLine()
            print('Required:')

        def printLine(self):
            print('====================================================================')

    def Login():
        userKeys = ['-u', '--username']
        passKeys = ['-p', '--password']

        tries = 3
        user = input('Username: ')
        for _ in range(tries):
            try:
                password = getpass()
            except KeyboardInterrupt:
                return

            if limes.Login(user, password):
                return
        return '%s failed attempts, check your connection and credentials' % tries

    def Add():
        if len(args) == 5:
            limes.Add(args[2], args[1], args[4])
        elif len(args) == 3:
            limes.Add(args[2], args[1])
        else:
            return 'usage: limes add [file path] [sampleId] (-as [name])'
        return ''

    def Search():
        try:
            if not limes._auth(): return
        except:
            return

        if len(args) < 2:
            return 'usage: Search [tokens], where [tokens] is any string'

        query = ""
        for arg in args[1:]:
            query += arg + " "
        samples = limes.Search(query)
        count = len(samples)
        msg = '%s result%s found' % (count, 's' if count != 1 else '')
        max = 3
        if count > max: msg += ', truncating to first %s' % max
        i = 1
        for sample in samples:
            msg += '\n'
            # msg += '\n%s of %s' % (i, count)
            msg += '\nID: %s\nName: %s' % (sample.Id, sample.Name)
            msg += '\n%smembers/inventory/browser/?sampleID=%s#viewSample' % (config.ELAB_URL, sample.Id)
            i += 1
            if i > max: break
        return msg

    def Blast():
        try:
            if not limes._auth(): return
        except:
            return

        if len(args) != 2:
            return 'usage: Blast [query], where [query] is a valid .fasta for blast queries'

        print(limes.Blast(args[1]))
        return

    def _printHelp(unkownArg=False):
        msg = 'use [-h] or [--help] to view options\nor view available documentation at https://github.com/Tony-xy-Liu/Limes/'
        if unkownArg:
            msg = '[%s] was not recognized\n%s' % (unkownArg, msg)
        return msg

    def _getVal(keys: List[str], args: List[str]) -> tuple[bool, str]:
        next = 1
        for item in args:
            if item in keys and next < len(args):
                return True, args[next]
            next +=1
        return False, ""

    arg = args[0] if len(args) > 0 else ''

    def base():
        print(Constants.version)
        limes._auth()

    # the switch doesn't need to be fast, make it easier to make
    # also need to add hints here
    return Switch(arg, {
        '': base,
        '-h': lambda: Constants.help,
        '--help': lambda: Constants.help,
        'login': Login,
        'dlogin': lambda: limes.dLogin(),
        'search': Search,
        'blast': Blast,
        'add': Add,
        'test': lambda: limes.Test(),
    }, lambda: _printHelp(arg))

if __name__ == "__main__":
    try:
        end = main()
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        end = None
    if not end is None and end != '':
        sys.exit(end)
    else:
        sys.exit()