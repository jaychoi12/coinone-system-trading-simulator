from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^account/$', views.account, name='account'),
    url(r'^simulator/$', views.simulator, name='simulator'),
    url(r'^simulator/(?P<currency_name>[\w]+)/$', views.chart, name='chart'),
    url(r'^simulator/(?P<currency_name>[\w]+)/logs/$', views.logs, name='logs'),
]
