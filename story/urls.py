# from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'story'

urlpatterns = [
    url('^$', views.Top.as_view(), name='top'),
    url('^user/login/$', views.Login.as_view(), name='login'),
    url('^user/logout/$', views.Logout.as_view(), name='logout'),
    url('^user/profile/edit/$', views.edit_profile, name='edit_profile'),
    url('^user/profile/$', views.user_profile_view, name='profile'),
    url('^user/create/$', views.CreateUserView.as_view(), name='create'),
    url('^story/list/$', views.story_list, name='story_list'),
    url('^story/create/$', views.start_story, name='new_story'),
    url('^story/(?P<story_id>[0-9]+)/$', views.show_story, name='show_story'),
    url('^story/(?P<story_id>[0-9]+)/vote$', views.add_nice, name='add_vote'),
    url('^entry/add/(?P<story_id>[0-9]+)/$', views.write_entry, name='add_story_entry'),
    url('^entry/add/$', views.write_entry, name='new_story_entry'),
    url('^story/(?P<story_id>[0-9]+)/comment/', views.comment_page, name='comment_page'),
    url('^entry/list/(?P<page>[0-9]+)/$', views.entry_list, name='entry_list'),
]
