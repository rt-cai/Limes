from django.urls import path
from django.urls.resolvers import URLPattern

from limes_common.models.server import Endpoints
from limes_common import config
from . import views

def genPath(ep: str) -> URLPattern:
    return path('%s/%s' % (config.SERVER_API_VER, ep), views.__dict__[ep.title()], name=ep)

# urlpatterns = [
#     path('%s/login' % VER, views.Login, name='login'),
#     path('%s/authenticate' % VER, views.Authenticate, name='authenticate'),
# ]

urlpatterns = list(map(genPath, Endpoints.Paths()))
