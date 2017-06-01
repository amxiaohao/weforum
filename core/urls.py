from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.settings, name='settings'),
    url(r'^password/$', views.password, name='password'),
    url(r'^picture/$', views.upload_picture, name='upload_picture'),
]