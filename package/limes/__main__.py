import sys

if sys.argv[1] == '-test': 
    print('######################################################')
    print('begin tests')
    print('######################################################')

    from .tests import models
    # from .tests import sshConnection
    # from .tests import elab
    # from .tests import limes