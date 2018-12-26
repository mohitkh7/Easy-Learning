from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
# from .views import TopicList,home,TopicDetails,TopicCreate,TopicUpdate,TopicDelete,ResourceCreate,ResourceUpdate,ResourceDelete,ReviewCreate,ReviewUpdate,ReviewDelete,SignupView, myaccount, UserUpdate, AllActivityList
from .views import *
#from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,password_reset_done,password_reset,password_reset_confirm,password_reset_complete,PasswordChangeView,PasswordChangeDoneView
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView,PasswordChangeView,PasswordChangeDoneView
from .decorators import strictly_no_login
from django.urls import path

urlpatterns=[
	#url(r'^$',index,name="index"),
	path('',index,name='index'),
	#url(r'^home/$',home,name="search"),
	path('home/',home,name='search'),
	#url(r'^all-activity/$',AllActivityList.as_view(),name="activity"),
	path('all-activity/',AllActivityList.as_view(),name="activity"),

	#url(r'^myaccount/$',myaccount,name="myaccount"),
	path('myaccount/',myaccount,name="myaccount"),
	#url(r'^myaccount/change/$',UserUpdate.as_view(),name="UserUpdate"),
	path('myaccount/change/',UserUpdate.as_view(),name="UserUpdate"),

	#url(r'^topic/all/$',TopicList.as_view(),name="TopicList"),
	path('topic/all/',TopicList.as_view(),name="TopicList"),

	#url(r'^(?P<topic_slug>[-\w]+)/add-resource/',ResourceCreate.as_view(),name="ResourceCreate"),
	path('<slug:topic_slug>/add-resource/',ResourceCreate.as_view(),name="ResourceCreate"),
	#url(r'^(?P<topic_slug>[-\w]+)/update-resource/(?P<slug>[-\w]+)/',ResourceUpdate.as_view(),name="ResourceUpdate"),
	path('<slug:topic_slug>/update-resource/<slug:slug>/',ResourceUpdate.as_view(),name="ResourceUpdate"),
	#url(r'^topic/(?P<topic_slug>[-\w]+)/delete-resource/(?P<slug>[-\w]+)/',ResourceDelete.as_view(),name="ResourceDelete"),
	path('topic/<slug:topic_slug>/delete-resource/<slug:slug>/',ResourceDelete.as_view(),name="ResourceDelete"),
	#url(r'^(?P<topic_slug>[-\w]+)/(?P<slug>[-\w]+)/bookmark-resource/',ResourceBookmark,name="ResourceBookmark"),
	path('<slug:topic_slug>/<slug:slug>/bookmark-resource/',ResourceBookmark,name="ResourceBookmark"),
	
	#url(r'^add-topic/',TopicCreate.as_view(),name="TopicCreate"),
	path('add-topic/',TopicCreate.as_view(),name="TopicCreate"),
	
	#url(r'^update-topic/(?P<slug>[-\w]+)/',TopicUpdate.as_view(),name="TopicUpdate"),
	path('update-topic/<slug:slug>/',TopicUpdate.as_view(),name="TopicUpdate"),
	
	#url(r'^remove-topic/(?P<slug>[-\w]+)/',TopicDelete.as_view(),name="TopicDelete"),
	path('remove-topic/<slug:slug>/',TopicDelete.as_view(),name="TopicDelete"),

	#url(r'^(?P<topic_slug>[-\w]+)/(?P<resource_slug>[-\w]+)/add-review/',ReviewCreate.as_view(),name="ReviewCreate"),
	path('<slug:topic_slug>/<slug:resource_slug>/add-review/',ReviewCreate.as_view(),name="ReviewCreate"),
	#url(r'^(?P<topic_slug>[-\w]+)/(?P<resource_slug>[-\w]+)/update-review/(?P<pk>[0-9]+)/',ReviewUpdate.as_view(),name="ReviewUpdate"),
	path('<slug:topic_slug>/<slug:resource_slug>/update-review/<int:pk>/',ReviewUpdate.as_view(),name="ReviewUpdate"),
	
	#url(r'^(?P<topic_slug>[-\w]+)/(?P<resource_slug>[-\w]+)/delete-review/(?P<pk>[0-9]+)/',ReviewDelete.as_view(),name="ReviewDelete"),
	path('<slug:topic_slug>/<slug:resource_slug>/delete-review/<int:pk>/',ReviewDelete.as_view(),name="ReviewDelete"),

	#url(r'^(?P<topic_slug>[-\w]+)/(?P<resource_slug>[-\w]+)/(?P<action>[-\w]+)/',managevote,name="vote"),
	path('<slug:topic_slug>/<slug:resource_slug>/<slug:action>/',managevote,name="vote"),

	#url(r'^category/all/$',CategoryList.as_view(),name="CategoryList"),
	path('category/all/',CategoryList.as_view(),name="CategoryList"),
	#url(r'^category/(?P<category_slug>[-\w]+)/$',SelectedTopicList.as_view(),name="SelectedTopicList"),
	path('category/<slug:category_slug>/',SelectedTopicList.as_view(),name="SelectedTopicList"),
	#url(r'^ajaxcall/topicautocomplete/',autocompleteSuggestionTopic,name="AjaxTopicAutocomplete"),
	path('ajaxcall/topicautocomplete/',autocompleteSuggestionTopic,name="AjaxTopicAutocomplete"),

]

urlpatterns+=[
	#url(r'^login/',LoginView.as_view(redirect_authenticated_user=True),name="login"),
	path('login/',LoginView.as_view(redirect_authenticated_user=True),name="login"),
	#url(r'^logout/',LogoutView.as_view(),name="logout"),		
	path('logout/',LogoutView.as_view(),name="logout"),
	#url(r'signup/',SignupView.as_view(),name="signup"),
	path('signup/',SignupView.as_view(),name="signup"),

	#url(r'^myaccount/change_password',PasswordChangeView.as_view(),name="change_password"),
	path('myaccount/change_password',PasswordChangeView.as_view(),name="change_password"),
	
	#url(r'^myaccount/password_change_done/',PasswordChangeDoneView.as_view(),name="password_change_done"),
	path('myaccount/password_change_done/',PasswordChangeDoneView.as_view(),name="password_change_done"),

	#url(r'^forgot_password/$',strictly_no_login(PasswordResetView.as_view()),name="forgot_password"),
	path('forgot_password/',strictly_no_login(PasswordResetView.as_view()),name="forgot_password"),
	#url(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    #url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view, name='password_reset_confirm'),
    path('reset/<slug:uidb64>/<str:token>/',PasswordResetConfirmView.as_view, name='password_reset_confirm'),
    #url(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
#to avoid errors
urlpatterns+=[
	#url(r'^(?P<slug>[-\w]+)/$',TopicDetails.as_view(),name="TopicDetails"),
	path('<slug:slug>/',TopicDetails.as_view(),name="TopicDetails"),
	url(r'^(?P<slug>[-\w]+)/test.$',test,name="test"),
	#path('<slug:slug>/test.$',test,name="test"),
]
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)