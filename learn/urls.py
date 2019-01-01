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
	
	path('',index,name='index'),
	path('home/',home,name='search'),
	path('all-activity/',AllActivityList.as_view(),name="activity"),

	path('myaccount/',myaccount,name="myaccount"),
	path('myaccount/change/',UserUpdate.as_view(),name="UserUpdate"),

	path('topic/all/',TopicList.as_view(),name="TopicList"),

	path('<slug:topic_slug>/add-resource/',ResourceCreate.as_view(),name="ResourceCreate"),
	path('<slug:topic_slug>/update-resource/<slug:slug>/',ResourceUpdate.as_view(),name="ResourceUpdate"),
	path('topic/<slug:topic_slug>/delete-resource/<slug:slug>/',ResourceDelete.as_view(),name="ResourceDelete"),
	path('<slug:topic_slug>/<slug:slug>/bookmark-resource/',ResourceBookmark,name="ResourceBookmark"),
	
	path('add-topic/',TopicCreate.as_view(),name="TopicCreate"),
	
	path('update-topic/<slug:slug>/',TopicUpdate.as_view(),name="TopicUpdate"),
	
	path('remove-topic/<slug:slug>/',TopicDelete.as_view(),name="TopicDelete"),

	path('<slug:topic_slug>/<slug:resource_slug>/add-review/',ReviewCreate.as_view(),name="ReviewCreate"),
	path('<slug:topic_slug>/<slug:resource_slug>/update-review/<int:pk>/',ReviewUpdate.as_view(),name="ReviewUpdate"),
	
	path('<slug:topic_slug>/<slug:resource_slug>/delete-review/<int:pk>/',ReviewDelete.as_view(),name="ReviewDelete"),

	path('<slug:topic_slug>/<slug:resource_slug>/<slug:action>/',managevote,name="vote"),


	path('category/all/',CategoryList.as_view(),name="CategoryList"),
	path('category/<slug:category_slug>/',SelectedTopicList.as_view(),name="SelectedTopicList"),
	path('ajaxcall/topicautocomplete/',autocompleteSuggestionTopic,name="AjaxTopicAutocomplete"),

	path('youtubeResource/',youtubeResource,name="youtubeResource"),
	path('youtubeResourcePreview/',youtubeResourcePreview,name="youtubeResourcePreview"),


urlpatterns+=[
	path('login/',LoginView.as_view(redirect_authenticated_user=True),name="login"),
	path('logout/',LogoutView.as_view(),name="logout"),
	path('signup/',SignupView.as_view(),name="signup"),

	path('myaccount/change_password',PasswordChangeView.as_view(),name="change_password"),
	
	path('myaccount/password_change_done/',PasswordChangeDoneView.as_view(),name="password_change_done"),

	path('forgot_password/',strictly_no_login(PasswordResetView.as_view()),name="forgot_password"),
	path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<slug:uidb64>/<str:token>/',PasswordResetConfirmView.as_view, name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
#to avoid errors
urlpatterns+=[
	path('<slug:slug>/',TopicDetails.as_view(),name="TopicDetails"),
	path('<slug:slug>/test',test,name="test"),
]
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)