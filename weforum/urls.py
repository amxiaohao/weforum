from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from core import views as core_views
from search import views as search_views
from authentication import views as authentication_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', core_views.home, name='home'),
    url(r'^signup/$', authentication_views.signup, name='signup'),
    url(r'^login/$', auth_views.login, 
        {'template_name': 'core/cover.html', 'redirect_field_name': '/'}, name='login'),
    url(r'^logout/$', auth_views.logout, 
        {'next_page': '/'}, name='logout'),

    url(r'^articles/', include('articles.urls', namespace='articles')),
    url(r'^settings/', include('core.urls', namespace='core')),
    url(r'^search/$', search_views.search, name='search'),
    url(r'^(?P<username>[0-9a-zA-Z_]+)/$', core_views.profile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)