from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register, name='register'),
    url(r'^admin$', views.success, name='admin'),
    url(r'^login$', views.userlogin, name='login'),
    url(r'^update$', views.update, name='update'),
    url(r'^delete$', views.delete, name='delete'),
    url(r'^insert$', views.insert, name='insert'),
    url(r'^insertpublisher$', views.insertpublisher, name='insertpublisher'),
    url(r'^insertapi$', views.insertapi, name='insertapi'),
    url(r'^updateapi$', views.updateapi, name='updateapi'),
    url(r'^updatepublisher$', views.updatepublisher, name='updatepublisher'),
    url(r'^deleteapi$', views.deleteapi, name='deleteapi'),
    url(r'^home$', views.home, name='home'),
    url(r'^userlogout$', views.userlogout, name='userlogout'),
    url(r'^dev$', views.dev, name='dev'),
]
