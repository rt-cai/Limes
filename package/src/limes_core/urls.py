from django.urls import path

from . import views

VER = 'd1'
urlpatterns = [
    path('%s' % VER, views.index, name='index'),
    path('%s/login' % VER, views.Login, name='login'),
]