import os
import inspect
import sys
from typing import Callable
from flask import Flask, request
from flask_socketio import SocketIO

import uuid

from limes_common import config
from limes_common.models import Model, server, elab
from .providers import Handler as ProviderHandler
from .clientManager import Client, ClientManager

app = Flask(__name__, static_url_path='', static_folder='public')
app.config['SECRET_KEY'] = 'secret'
sio = SocketIO(app)

_views: dict[str, Callable] = {}

def _toRes(model: Model):
    return model.ToDict()

_clientManager = ClientManager.GetInstance()
_providers = ProviderHandler(_views, _clientManager)

# todo: csrf + maybe encryption 
def Init():
    print('init')
    return _toRes(server.Init.Response('dummy token'))

def RegisterClient():
    SR = server.RegisterClient
    req = SR.Request.Parse(request.data)
    # print(request.data)
    if not _clientManager.RegisterClient(req): return _toRes(SR.Response(False))
    print('login: %s' % (req.FirstName))
    return _toRes(SR.Response(True))

def Authenticate():
    SA = server.Authenticate
    elab_res = SA.Request.Parse(request.data)
    client = _clientManager.Get(elab_res.ClientID)

    print('auth: %s' % (client.FirstName if client is not None else 'unknown'))
    res = SA.Response()
    if client is not None:
        res.Success = True
        res.Token = client.Token
        res.FirstName = client.FirstName
        res.LastName = client.LastName
    else:
        res.Success = False
    return _toRes(res)

def Login():
    SL = server.Login
    req = SL.Request.Parse(request.data)
    elab = _providers.GetElabCon()
    e_res = elab.Login(req.Username, req.Password)

    res = SL.Response()
    if e_res.token is not None and e_res.token != '':
        print('login: %s'  % e_res.user.firstName)
        reg = server.RegisterClient.Request()
        reg.ELabKey = e_res.token
        reg.FirstName = e_res.user.firstName
        reg.LastName = e_res.user.lastName
        reg.ClientID = '%012x' % (uuid.uuid1().int)
        _clientManager.RegisterClient(reg)
        
        res.FirstName = reg.FirstName
        res.LastName = reg.LastName
        res.ClientID = reg.ClientID
        res.Success = True
        res.Code = 200
    else:
        res.Success = False
        res.Code = e_res.Code

    elab.Logout()
    return _toRes(res)

def Barcodes():
    SB = server.BarcodeLookup
    req = SB.Request.Parse(request.data)
    client = _clientManager.Get(req.ClientID)

    res = SB.Response()

    if client is not None:
        elab = _providers.GetElabCon()
        elab.SetAuth(client.Token)
        res.Results = elab.LookupBarcodes(req.Barcodes)
        elab.Logout()
    else:
        res.Code = 401
        res.Error = 'Authentication failed'

    return _toRes(res)
    # return {}

def AllStorages():
    MODEL = server.AllStorages
    req = MODEL.Request.Parse(request.data)
    client = _clientManager.Get(req.ClientID)
    res = MODEL.Response()

    if client is not None:
        elab = _providers.GetElabCon()
        elab.SetAuth(client.Token)
        res.Results = elab.GetAllStorages()
        elab.Logout()
    else:
        res.Code = 401
        res.Error = 'Authentication failed'

    return _toRes(res)

def SamplesByStorage():
    MODEL = server.SamplesByStorage
    req = MODEL.Request.Parse(request.data)
    client = _clientManager.Get(req.ClientID)

    res = MODEL.Response()

    if client is not None:
        elab = _providers.GetElabCon()
        elab.SetAuth(client.Token)
        res.Results = elab.GetSampleByStorage(req.StorageLayerID).data
        elab.Logout()
    else:
        res.Code = 401
        res.Error = 'Authentication failed'

    return _toRes(res)

_printReports = {}
_printInfo = {}
def PrintOps():
    SP = server.Printing
    req = SP.BaseRequest.Parse(request.data)
    OPS = server.PrintOp
    res = SP.Response()

    getID = lambda: '%012x' % (uuid.uuid1().int)
    INFO_ID = 'infoid'
    if req.Op == OPS.PRINT:
        pr = SP.PrintRequest.Parse(request.data, base=req)
        pr.ID = getID()
        sio.emit('print', pr.ToDict())
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