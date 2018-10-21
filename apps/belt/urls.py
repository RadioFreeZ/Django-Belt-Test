from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.dash, name="dash"),
    url(r'^register/$', views.register, name="register"),
    url(r'^login/$', views.login, name="login"),
    url(r'^logout/$', views.logout, name="logout"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^jobs/edit/(?P<id>\d+)$', views.edit, name="edit"),
    url(r'^jobs/update/(?P<id>\d+)$', views.update, name="update"),
    url(r'^jobs/new/$', views.new, name="new"),
    url(r'^jobs/create/$', views.create, name="create"),
    url(r'^jobs/(?P<id>\d+)/$', views.view, name="view"),
    url(r'^jobs/add/(?P<id>\d+)$', views.add, name="add"),
    url(r'^jobs/delete/(?P<id>\d+)/$', views.delete, name="delete"),
    url(r'^jobs/give/(?P<id>\d+)/$', views.give, name="give"),
]
