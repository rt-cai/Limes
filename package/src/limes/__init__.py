from . import limes

import sys
from typing import List
from getpass import getpass

from .tools.qol import Switch

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
            tries = 3
            user = input('Username: ')
            for _ in range(tries):
                try:
                    password = getpass()
                except KeyboardInterrupt:
                    return

                if limes.Login(user, password):
                    return
            print('%s failed attempts, check your connection and credentials' % tries)

    class Test():
        def __init__(self) -> None:
            limes.Test()
            pass

    def __init__(self, args: List[str] = None) -> None:
        if args is None:
            args = sys.argv[1:]

        arg = args[0] if len(args) > 0 else ""
        def help():
            from .res import help
            print(help.msg)

        Switch(arg,{
            '--help': help,
            '-h': help,
            'login': lambda: self.Login(args[1:]),
            'test': lambda: self.Test()
        },
        lambda: Console._printHelp(arg))

    @staticmethod
    def _printHelp(unkownArg=False):
        msg = 'use [-h] or [--help] to view options\nor view available documentation at https://github.com/Tony-xy-Liu/Limes/'
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

