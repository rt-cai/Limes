import os
import inspect
import sys
from typing import Callable
from flask import Flask, request
from flask_socketio import SocketIO

import uuid

from limes_common import config
from limes_common.models import Model, server, elab
from limes_common.utils import format_from_utc, current_time
from server.authenticator import Authenticator
from .providers import Handler as ProviderHandler
from .clientManager import Client, ClientManager

app = Flask(__name__, static_url_path='', static_folder='public')
def getSecret():
    secret_path = 'server/secret'
    try:
        with open(secret_path, 'r') as s:
            return s.readlines()[0][:-1]
    except FileNotFoundError:
        import secrets
        with open(secret_path, 'w') as s:
            tok = secrets.token_urlsafe(64)
            s.write(tok)
            s.flush()
            return tok
app.config['SECRET_KEY'] = getSecret()
sio = SocketIO(app)

_views: dict[str, Callable] = {}

def _toRes(model: Model):
    return model.ToDict()


_providers = ProviderHandler(_views, ClientManager.GetInstance())
_authenticator = Authenticator(_providers.GetElabCon())

# todo: csrf + maybe encryption 
def Init():
    print('init session')
    return _toRes(server.Init.Response('dummy token'))

def Authenticate():
    MODEL = server.Authenticate
    req = MODEL.Request.Parse(request.data)
    res = _authenticator.Authenticate(req.ClientID)
    if res.Success:
        print('auth: %s' % (res.FirstName))
    return _toRes(res)

def Login():
    res = _authenticator.Login(request.data)
    if res.Success:
        print('login: %s'  % res.FirstName)
    return _toRes(res)

def Barcodes():
    SB = server.BarcodeLookup
    req = SB.Request.Parse(request.data)
    auth = _authenticator.Authenticate(req.ClientID)

    res = SB.Response()

    if auth.Success:
        elab = _providers.GetElabCon()
        elab.SetAuth(auth.Token)
        res.Results = elab.LookupBarcodes(req.Barcodes)
        elab.Logout()
    else:
        res.Code = 401
        res.Error = 'Authentication failed'

    return _toRes(res)
    # return {}

def SetAltID():
    MODEL = server.LinkBarcode
    req = MODEL.Request.Parse(request.data)
    auth = _authenticator.Authenticate(req.ClientID)

    res = MODEL.Response()
    if auth.Success:
        print('altid')
        elab = _providers.GetElabCon()
        elab.SetAuth(auth.Token)
        res.Code, res.Sample = elab.SetAltID(req.SampleBarcode, req.AltBarcode)
        elab.Logout()
    else:
        res.Code = 401
        res.Error = 'Authentication failed'

    return _toRes(res)

def AllStorages():
    MODEL = server.AllStorages
    req = MODEL.Request.Parse(request.data)
    auth = _authenticator.Authenticate(req.ClientID)
    res = MODEL.Response()

    if auth.Success:
        elab = _providers.GetElabCon()
        elab.SetAuth(auth.Token)
        res.Results = elab.GetAllStorages()
        elab.Logout()
    else:
        res.Code = 401
        res.Error = 'Authentication failed'

    return _toRes(res)

def SamplesByStorage():
    MODEL = server.SamplesByStorage
    req = MODEL.Request.Parse(request.data)
    auth = _authenticator.Authenticate(req.ClientID)

    res = MODEL.Response()

    if auth.Success:
        elab = _providers.GetElabCon()
        elab.SetAuth(auth.Token)
        res.Results = elab.GetSampleByStorage(req.StorageLayerID).data
        elab.Logout()
    else:
        res.Code = 401
        res.Error = 'Authentication failed'

    return _toRes(res)

_printReports = {}
_printInfo = {}

def _log(msg: str):
    with open("log.txt", "a") as myfile:
        myfile.write('%s\n'% msg)

def PrintOps():
    SP = server.Printing
    req = SP.BaseRequest.Parse(request.data)
    OPS = server.PrintOp
    res = SP.Response()

    cl = _authenticator.Authenticate(req.ClientID)
    if not cl.Success:
        res.Code = 401
        return _toRes(res)

    getID = lambda: '%012x' % (uuid.uuid1().int)
    INFO_ID = 'infoid'
    if req.Op == OPS.PRINT:
        pr = SP.PrintRequest.Parse(request.data, base=req)
        pr.ID = getID()
        
        for l in pr.Labels:
            if l.Barcode == '':
                l.Barcode = '0'

        sio.emit('print', pr.ToDict())
        log = '%s| print: %s, %s, %s, %s' % (format_from_utc(current_time()), cl.FirstName, len(pr.Labels), pr.TemplateName, pr.PrinterName)
        _log(log)
        res.ID = pr.ID

    elif req.Op == OPS.REFRESH_INFO:
        sio.emit('printers', {})
        sio.emit('templates', {})
        res.ID = INFO_ID
    elif req.Op == OPS.POLL:
        pr = SP.PollReport.Parse(request.data, base=req)
        res = SP.Report()

        if pr.ID == INFO_ID:
            res.Data = _printInfo
            res.Success = True
        else:
            def check(d):
                m =  d.get(pr.ID, None)
                if m is not None:
                    del d[pr.ID]
                return m

            m = check(_printReports)
            res.Success = m is not None
            if m is not None:
                res.Data = {'Message': m}
    else:
        res.Code = 400
        print('x')
 
    return _toRes(res)

def add_Api_Views():
    current_module = sys.modules[__name__]
    views = _views
    for n, view in inspect.getmembers(current_module, inspect.isfunction):
        if not n.startswith('_') and n[0].title() == n[0]:
            views[n.lower()] = view

    print('## loading api endpoints')
    linked = 0
    paths = server.Endpoints.Paths()
    for name in paths:
        view = views.get(name, None)
        if view is None:
            print('unlinked endpoint [%s]'%name)
            continue
        else:
            del views[name]
        ep = '%s%s' % (config.SERVER_API_ENDPOINT, name)
        # todo, add methods to endpoint class
        if name in ['init', 'list']:
            m = 'GET'
        else:
            m = 'POST'    
        app.add_url_rule(ep, methods = [m], view_func=view)
        linked += 1
        # print('%s: %s' % (ep, m))
    for n in views.keys():
        print('unlinked view [%s]'%n)

    print('%s endpoints linked' % linked)
    if linked != len(paths):
        print('views: [%s]' % views)
add_Api_Views()

# website

@app.route('/')
def Home():
    return app.send_static_file('index.html')

@app.route('/forcefavicon')
def ForceFavicon():
    return app.send_static_file('favicon.ico')

# peripherals

_ccount = 0
@sio.on('connect')
def clientConnected(auth=None):
    global _ccount
    _ccount += 1
    print('sio client connect, auth [%s], total: %s' % (auth, _ccount))

@sio.on('disconnect')
def clientDiconnect(auth=None):
    global _ccount
    _ccount -= 1
    print('sio client disconnect, auth [%s], total: %s' % (auth, _ccount))

@sio.on('printReport')
def PrintReport(data):
    _printReports[data['ID']] = data['Message']


@sio.on('printers')
def listPrinters(data):
    _printInfo['printers'] = data['printers']

@sio.on('templates')
def listTemplates(data):
    _printInfo['templates'] = data['templates']