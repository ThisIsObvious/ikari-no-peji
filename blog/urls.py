from django.conf.urls import url
from django.conf.urls import patterns
from django.conf import settings
from . import views
from httpproxy.views import HttpProxy

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<num>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<num>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<num>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^manga/(?P<num>[0-9]+)/$',views.manga_general, name='manga_general'),
    url(r'^(?P<manga>[0-9]+)/(?P<numb>[0-9]+)/$', views.manga_page, name='manga_page'),
    url(r'^shop/$', views.shop, name='shop')
] 
if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'pages/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
)
    urlpatterns += patterns('',
    (r'^proxy/(?P<url>.*)$',
        HttpProxy.as_view(base_url='http://www.python.org/')),
)

