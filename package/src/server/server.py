import os
import inspect
import sys
from typing import Callable
from flask import Flask, request
from flask.helpers import send_from_directory

from limes_common import config
from limes_common.models import Model, server
from .providers import Handler as ProviderHandler

app = Flask(__name__, static_url_path='', static_folder='public')

_views: dict[str, Callable] = {}

def _toRes(model: Model):
    return model.ToDict()

class Client:
    # todo: add timeout
    def __init__(self, res: server.Login.Request) -> None:
        self.Token = res.ELabKey
        self.FirstName = res.FirstName
        self.LastName = res.LastName

_activeClients: dict[str, Client] = {}
_clientsByToken: dict[str, str] = {} # token: clientId
_providers = ProviderHandler(_views)

# todo: csrf + maybe encryption 
def Init():
    print('init')
    return _toRes(server.Init.Response('dummy token'))

def Login():
    SL = server.Login
    res = SL.Request.Parse(request.data)
    # print(request.data)

    # remove old if exists
    old = _clientsByToken.get(res.ELabKey)
    if old is not None: 
        _activeClients.pop(old)
        _clientsByToken.pop(res.ELabKey)

    if res.FirstName is None or res.LastName is None:
        return _toRes(SL.Response(False))

    _activeClients[res.ClientId] = Client(res)
    _clientsByToken[res.ELabKey] = res.ClientId

    print('login: %s' % (res.FirstName))
    return _toRes(SL.Response(True))

def Authenticate():
    SA = server.Authenticate
    elab_res = SA.Request.Parse(request.data)
    client = _activeClients.get(elab_res.ClientId)

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

def add_Api_Views():
    current_module = sys.modules[__name__]
    views = _views
    for n, view in inspect.getmembers(current_module, inspect.isfunction):
        if not n.startswith('_') and n.title() == n:
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
        if name == 'init':
            m = 'GET'
        else:
            m = 'POST'    
        app.add_url_rule(ep, methods = [m], view_func=view)
        linked += 1
    for n in views.keys():
        print('unlinked view [%s]'%n)

    print('%s endpoints linked' % linked)
    if linked != len(paths):
        print(views)
add_Api_Views()

# website

@app.route('/')
def Home():
    return app.send_static_file('index.html')

@app.route('/force/fav')
def favicon():
    return app.send_static_file('favicon.ico')