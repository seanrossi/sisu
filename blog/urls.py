from django.conf.urls import url
from . import views
from .views import IndexView

urlpatterns = [
    url(r'^$', views.about_sisu, name='about'),
    url(r'^about_us$', views.about_us, name='about_us'),
    url(r'^about_us/team$', views.about_team, name='about_team'),
    url(r'^about_us/empower_now$', views.about_program, name='about_program'),
    url(r'^post/$', views.post_list, name='post_list'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^drafts/$', views.post_draft_list, name='post_draft_list'),
    url(r'^post/(?P<pk>\d+)/publish/$', views.post_publish, name='post_publish'),
    url(r'^post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^comment/(?P<pk>\d+)/approve/$', views.comment_approve, name='comment_approve'),
    url(r'^comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),
    url(r'^post/category/(?P<category_name>\w+)$', views.post_list_by_category, name='post_list_by_category'),
    url(r'^cases$', views.post_cases, name='post_cases'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^sisu_case/category/(?P<category_name>\w+)$', views.story, name='story'),
    url(r'^sisu_case/(?P<pk>\d+)/$', views.story_entry, name='story_entry'),
    url(r'^user_details/user_id/(?P<pk>\d+)/$', views.user_details, name='user_details'),
    url(r'^likepost/$', views.on_off_star, name='on_off_star'),
    url(r'^add_comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    url(r'^add_reply_to_comment$', views.add_reply_to_comment, name='add_reply_to_comment'),
    url(r'^search$', views.search, name='search'),
    url(r'^settings/user_id(?P<pk>\d+)/$', IndexView.as_view(), name='user_details'),
    url(r'^terms_conditions/$', views.terms_conditions, name='t_c'),
    url(r'^privacy_policy/$', views.privacy_policy, name='p_p'),
    
]