from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^article/(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^archives/$', views.ArchivesView.as_view(), name='archives'),
    url(r'^aboutme/$', views.about_me, name='about_me'),
    url(r'^category/(?P<cate_id>\d+)/$', views.CategoryView.as_view(), name='category'),
    url(r'tag/(?P<tag_id>\d+)$', views.TagView.as_view(), name='tag'),
    url(r'^search/$', views.blog_search, name='blog_search'),
    url(r'^feed/$', views.RSSFeed(), name = "RSS"), 
]
