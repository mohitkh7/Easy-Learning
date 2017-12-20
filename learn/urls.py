from django.conf.urls import url
# from .views import TopicList,home,TopicDetails,TopicCreate,TopicUpdate,TopicDelete,ResourceCreate,ResourceUpdate,ResourceDelete,ReviewCreate,ReviewUpdate,ReviewDelete,SignupView, myaccount, UserUpdate, AllActivityList
from .views import *
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,password_reset_done,password_reset,password_reset_confirm,password_reset_complete,PasswordChangeView,PasswordChangeDoneView
from .decorators import strictly_no_login



urlpatterns=[
	url(r'^$',search,name="search"),
	url(r'^home/$',home,name="home"),
	url(r'^activity/$',AllActivityList.as_view(),name="activity"),

	url(r'^myaccount/$',myaccount,name="myaccount"),
	url(r'^myaccount/change/$',UserUpdate.as_view(),name="UserUpdate"),

	url(r'^category/all/$',CategoryList.as_view(),name="CategoryList"),
	url(r'^category/(?P<category_slug>[-\w]+)/$',SelectedTopicList.as_view(),name="SelectedTopicList"),

	# url(r'^cat/(?P<category_slug>[-\w]+)/(?P<topic_slug>[-\w])/$',ResourceList.as_view(),name="ResourceList"),
	
	url(r'^topic/all/$',TopicList.as_view(),name="TopicList"),
	url(r'^topic/create/',TopicCreate.as_view(),name="TopicCreate"),
	url(r'^(?P<category_slug>[-\w]+)/(?P<slug>[-\w]+)/$', TopicDetails.as_view(), name='TopicDetails'),
	url(r'^topic/(?P<slug>[-\w]+)/update/',TopicUpdate.as_view(),name="TopicUpdate"),
	url(r'^topic/(?P<slug>[-\w]+)/delete/',TopicDelete.as_view(),name="TopicDelete"),

	url(r'^topic/(?P<topic_slug>[-\w]+)/resource/add/',ResourceCreate.as_view(),name="ResourceCreate"),
	url(r'^topic/(?P<topic_slug>[-\w]+)/resource/(?P<slug>[-\w]+)/update/',ResourceUpdate.as_view(),name="ResourceUpdate"),
	url(r'^topic/(?P<topic_slug>[-\w]+)/resource/(?P<slug>[-\w]+)/delete/',ResourceDelete.as_view(),name="ResourceDelete"),
	url(r'^topic/(?P<topic_slug>[-\w]+)/resource/(?P<slug>[-\w]+)/bookmark/',ResourceBookmark,name="ResourceBookmark"),

	url(r'^topic/(?P<topic_slug>[-\w]+)/resource/(?P<resource_slug>[-\w]+)/review/add/',ReviewCreate.as_view(),name="ReviewCreate"),
	url(r'^topic/(?P<topic_slug>[-\w]+)/resource/(?P<resource_slug>[-\w]+)/review/update/(?P<pk>[0-9]+)/',ReviewUpdate.as_view(),name="ReviewUpdate"),
	url(r'^topic/(?P<topic_slug>[-\w]+)/resource/(?P<resource_slug>[-\w]+)/review/delete/(?P<pk>[0-9]+)/',ReviewDelete.as_view(),name="ReviewDelete"),

	url(r'learn/(?P<resource_slug>[-\w]+)/vote/(?P<action>[-\w]+)/',managevote,name="vote"),
]

urlpatterns+=[
	url(r'^login/',LoginView.as_view(redirect_authenticated_user=True),name="login"),
	url(r'^logout/',LogoutView.as_view(),name="logout"),		
	url(r'signup/',SignupView.as_view(),name="signup"),

	url(r'^myaccount/change_password',PasswordChangeView.as_view(),name="change_password"),
	url(r'^myaccount/password_change_done/',PasswordChangeDoneView.as_view(),name="password_change_done"),

	url(r'^forgot_password/$',strictly_no_login(PasswordResetView.as_view()),name="forgot_password"),
	url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),


]
# urlpatterns += staticfiles_urlpatterns()
