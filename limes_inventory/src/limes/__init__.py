from . import limes

import sys
from typing import List
from getpass import getpass

from limes_common.tools.qol import Switch

class Console:
    class Command:
        def __init__(self, schemas, options) -> None:
            self.schemas = schemas
            self.options = options

        def printHelp(self):
            self.printLine()
            print('Required:')

        def printLine(self):
            print('====================================================================')

    class Login():
        userKeys = ['-u', '--username']
        passKeys = ['-p', '--password']

        def __init__(self, args) -> None:
            try:
                user = input('Username: ')
                password = getpass()
            except KeyboardInterrupt:
                return

            limes.Login(user, password)

    class Test():
        def __init__(self) -> None:
            limes.Test()
            pass

    def __init__(self, args: List[str] = None) -> None:
        if args is None:
            args = sys.argv[1:]

        arg = args[0] if len(args) > 0 else ""
        Switch(arg,{
            '-h, --help': lambda: print("lists options. Full documentation at https://github.com/Tony-xy-Liu/Limes/\nuse with limes [command] -h to get sub options, example: limes login -h"),
            'login': lambda: self.Login(args[1:]),
            'test': lambda: self.Test()
        },
        lambda: Console._printHelp(arg))

    @staticmethod
    def _printHelp(unkownArg=False):
        msg = 'use [-h] or [--help] to view options or view available documentation at https://github.com/Tony-xy-Liu/Limes/'
        if unkownArg:
            msg = '[%s] was not recognized\n%s' % (unkownArg, msg)
        print(msg)

    @staticmethod
    def _getVal(keys: List[str], args: List[str]) -> tuple[bool, str]:
        next = 1
        for item in args:
            if item in keys and next < len(args):
                return True, args[next]
            next +=1
        return False, ""

def main():
    Console()
    
# Console()

