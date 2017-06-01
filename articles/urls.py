from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.articles, name='articles'),
    url(r'^write/$', views.write, name='write'),
    url(r'^draft/$', views.draft, name='draft'),
    url(r'^comment/(?P<article_id>[0-9]+)/$', views.comment, name='comment'),
    url(r'^tag/(?P<tag_name>.+)/$', views.tag, name='tag'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.edit, name='edit_article'),
    url(r'^(?P<slug>[-\w]+)/$', views.article, name='article'),
]