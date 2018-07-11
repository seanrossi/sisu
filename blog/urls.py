from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.about_sisu, name='about'),
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/category/(?P<category_name>\w+)$', views.post_list_by_category, name='post_list_by_category'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^settings/$', views.user_settings, name='user_settings'),
    url(r'^preference/(?P<voted_value>\d+)/$', views.vote_for_app, name='vote_for_app'),
    url(r'^post/(?P<postid>\d+)/preference/(?P<on_off_value>\d+)/$', views.on_off_star, name='on_off_star'),
    url(r'^search$', views.search, name='search'),
]