from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new, name='new'),
    url(r'^create$', views.create, name='create'),
    url(r'^(?P<id>\d+)$', views.show, name='show'),
    url(r'^users/(?P<id>\d+)$', views.show_user, name='show_user'),
]
