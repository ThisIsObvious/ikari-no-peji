from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<num>[0-9]+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<num>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<num>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^manga/(?P<num>[0-9]+)/$',view.manga_general, name='manga_general'),
    url(r'^manga/(?P<num>[0-9]+)/page/(?P<num>[0-9]+)/$', view.manga_page, name='manga_page'),
]
