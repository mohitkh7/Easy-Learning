import json
from django.http import JsonResponse

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from django.contrib.admin.models import LogEntry
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView,FormView
from django.views.generic.edit import CreateView,UpdateView,DeleteView

from .decorators import strictly_no_login
from .models import *
from .forms import *

import urllib.request as urlreq
import json
import os
from startlearning.settings import YOUTUBE_API_KEY

# Create your views here.
class ImageUploadForm(forms.Form):
	"""Image upload form."""
	image = forms.ImageField()

def index(request):
	context = {}

	popular_topics = Topic.objects.all().order_by('-views')
	latest_topics = Topic.objects.all().order_by('-added_on')
	context['popular_topics'] = popular_topics
	context['latest_topics'] = latest_topics

	if request.method == "POST":
		topic_searched = request.POST['search']
		try:
			topic = Topic.objects.get(title__iexact=topic_searched)
			return redirect(reverse_lazy('TopicDetails',kwargs={'slug':topic.slug}))
		except:
			context['search_error'] = topic_searched + " not found"
	return render(request,"learn/index.html",context)


def search(request):
	return render(request,"learn/search.html")

def home(request):
	return HttpResponse("Om Gang Gapatye Namah")

class AllActivityList(ListView):
	model = LogEntry
	template_name = "learn/activity.html"

class SelectedTopicList(ListView):
	template_name = "learn/selected_topic_list.html"
	context_object_name = 'topics'
	category = ""#get_object_or_404(Category,slug=kwargs['category_slug'])

	#filtering queryset show limited topics
	def get_queryset(self,*args,**kwargs):
		#Redirect to all categories not 404
		self.category = get_object_or_404(Category,slug=self.kwargs['category_slug'])
		return Topic.objects.filter(category=self.category).order_by('-views')

	#pass aditional data to template
	def get_context_data(self, *args, **kwargs):
		context = super(SelectedTopicList, self).get_context_data(*args, **kwargs)
		context['category'] = self.category
		return context

class TopicList(ListView):
	model=Topic
	context_object_name = "all_topics"
	template_name="learn/topic_list.html"
	paginate_by = 6

class TopicDetails(DetailView):
	model=Topic
	template_name="learn/topic_details.html"
	context_object_name = 'topic'
	# form = ResourceFilterForm(request.GET)

	def get_object(self):
		object=super(TopicDetails,self).get_object()
		object.views+=1
		object.save()
		return object

	def get_context_data(self,*args,**kwargs):
		context = super(TopicDetails, self).get_context_data(*args,**kwargs)
		topic = super(TopicDetails,self).get_object()
		form = ResourceFilterForm(self.request.GET)

		#getting all resources
		all_resources = Resource.objects.filter(topic=topic)
		filtered_resources = all_resources.order_by('-score')

		#getting parameters
		level = self.request.GET.get('level', '')
		method = self.request.GET.get('method','')
		sort = self.request.GET.get('sort','')

		if level != '':
			filtered_resources = filtered_resources.filter(level=level)
		if method != '':
			filtered_resources = filtered_resources.filter(method=method)
		if sort != '':
			sort_lookup_table = {
				'vhl':'-score',
				'vlh':'score',
				'phl':'-price',
				'plh':'price',
				'dno':'-added_on',
				'don':'added_on',
			}
			key = sort_lookup_table.get(sort,'-score')
			filtered_resources = filtered_resources.order_by(key)

		context['all_resources'] = all_resources
		context['filtered_resources'] = filtered_resources
		context['form'] = form
		return context
		
@method_decorator(login_required,name="dispatch")
class TopicCreate(CreateView):
	model=Topic
	fields=['title','description','category',"image"]
	# template_name_suffix="_create_form"
	template_name="learn/topic_create.html"
	def get_form(self):
		form = super(TopicCreate, self).get_form()
		# the actual modification of the form

		form.instance.person = self.request.user.person
		return form

@method_decorator(login_required,name="dispatch")
class TopicUpdate(UpdateView):
	model=Topic
	fields=['title','description','image']
	template_name="learn/topic_update.html"

@method_decorator(login_required,name="dispatch")
class TopicDelete(DeleteView):
	model=Topic
	success_url=reverse_lazy("TopicList")

@method_decorator(login_required,name="dispatch")
class ResourceCreate(CreateView):
	model=Resource
	fields=['title','description','url','price','method','level']
	template_name="learn/resource_create.html"
	# intial={'title':Topic.objects.all()[0].title,}

	def get_form(self):
		form=super(ResourceCreate,self).get_form()
		topic_slug=self.kwargs['topic_slug']
		#Queryset to object conversion
		topic=Topic.objects.get(slug=topic_slug)
		form.instance.topic=topic
		form.instance.person=self.request.user.person
		return form

	#pass aditional data to template
	def get_context_data(self, *args, **kwargs):
		context = super(ResourceCreate, self).get_context_data(*args, **kwargs)
		topic_slug = self.kwargs['topic_slug']
		topic=Topic.objects.get(slug=topic_slug)
		context['topic'] = topic
		return context

@method_decorator(login_required,name="dispatch")
class ResourceUpdate(UpdateView):
	model=Resource
	fields=['title','description','url','price','method','level']
	template_name="learn/resource_update.html"

@method_decorator(login_required,name="dispatch")
class ResourceDelete(DeleteView):
	# topic_slug=kwargs['topic_slug']
	model=Resource
	template_name="learn/resource_confirm_delete.html"
	# success_url=reverse_lazy("TopicDetails",kwargs={'slug':topic_slug})

	def get_success_url(self):
		topic_slug=self.kwargs['topic_slug']
		return reverse_lazy("TopicDetails",kwargs={'slug':topic_slug})

@login_required
def ResourceBookmark(request,topic_slug,slug):
	person = Person.objects.get(user=request.user)
	res = Resource.objects.get(slug=slug)
	bookmark,created = Bookmark.objects.get_or_create(person=person,resource=res)
	if not created:
		bookmark.delete()
		
	return redirect('TopicDetails', topic_slug)
	


@method_decorator(login_required,name="dispatch")
class ReviewCreate(CreateView):
	model=Review
	template_name="learn/review_create.html"
	fields=['star','text']

	def get_form(self):
		form=super(ReviewCreate,self).get_form()
		resource_slug=self.kwargs['resource_slug']
		resource=Resource.objects.get(slug=resource_slug)
		form.instance.resource=resource
		form.instance.person=self.request.user.person
		return form

	def get_queryset(self):
		queryset=super(ReviewCreate,self).get_queryset()
		resource_slug=self.kwargs['resource_slug']
		res=Resource.objects.get(slug=resource_slug)
		if Review.object.get(resource=res,person=self.request.user.person):
			return redirect("TopicList")
		return queryset

	def get_context_data(self,*args,**kwargs):
		context = super(ReviewCreate, self).get_context_data(*args, **kwargs)
		resource_slug=self.kwargs['resource_slug']
		res=Resource.objects.get(slug=resource_slug)
		context['resource'] = res
		return context

@method_decorator(login_required,name="dispatch")
class ReviewUpdate(UpdateView):
	model=Review
	template_name="learn/review_update.html"
	fields=['star','text']

	#To ensure a user can't edit someone's else review
	def get_queryset(self):
		queryset=super(ReviewUpdate,self).get_queryset()
		queryset=queryset.filter(person=self.request.user.person)
		return queryset

@method_decorator(login_required,name="dispatch")
class ReviewDelete(DeleteView):
	# topic_slug=kwargs['topic_slug']
	model=Review
	template_name="learn/review_confirm_delete.html"
	# success_url=reverse_lazy("TopicDetails",kwargs={'slug':topic_slug})

	def get_success_url(self):
		topic_slug=self.kwargs['topic_slug']
		return reverse_lazy("TopicDetails",kwargs={'slug':topic_slug})

	#To ensure a user can't edit someone's else review
	def get_queryset(self):
		queryset=super(ReviewDelete,self).get_queryset()
		queryset=queryset.filter(person=self.request.user.person)
		return queryset

@method_decorator(strictly_no_login,name="dispatch")
class SignupView(FormView):
	form_class=SignupForm
	template_name="registration/signup.html"
	success_url="/topic/all"

	def form_valid(self,form):
		form.save()
		username=form.cleaned_data['username']
		password=form.cleaned_data['password1']
		user = authenticate(username=username, password=password)
		# send_mail(subject, message, from_email, to_list, fail_silently=True)
		subject = 'Thank You'
		message = 'Welcome to Easy-Learning!\n Thank You for Joining Us.\n Happy Learning!'
		from_email = settings.EMAIL_HOST_USER
		to_list = [form.email, settings.EMAIL_HOST_USER]
		send_mail(subject, message, from_email, to_list, fail_silently=True)
		login(self.request, user)
		return super(SignupView, self).form_valid(form)

@login_required
def myaccount(request):
	user=request.user
	person 			= Person.objects.get(user=user)
	reviews 		= Review.objects.filter(person=person)
	resources 		= Resource.objects.filter(person=person)
	bookmarks 		= Bookmark.objects.filter(person=person)
	context={
		'user':user,
		'reviews':reviews,
		'resources':resources,
		'bookmarks':bookmarks
	}
	if request.method == 'POST':
		form = ImageUploadForm(request.POST, request.FILES)
		if form.is_valid():
			user.profile_picture = form.cleaned_data['image']
			user.save()
			return HttpResponse('image upload success')
		else:
			return HttpResponse('Leave')

	return render(request,"learn/myaccount.html",context)

class UserUpdate(UpdateView):
	model 			= User
	fields 			= ['first_name','last_name']
	template_name 	= "learn/topic_update.html" 
	success_url 	= reverse_lazy("myaccount")
	def get_object(self):
		user = self.request.user
		return user

class CategoryList(ListView):
	model = Category
	template_name = "learn/category_list.html"
	context_object_name = "categories"

@login_required
def managevote(request,topic_slug,resource_slug,action):
	resource = Resource.objects.get(slug=resource_slug)
	person = Person.objects.get(user=request.user)

	if action == 'upvote':
		value = 1
	elif action == 'downvote':
		value = -1
	else:
		value = 0

	try:
		#if vote exist
		vote = Vote.objects.get(resource=resource,person=person)
		if vote.value != value:
			vote.value = value
			vote.save()
	except:
		#if vote doesnot exist
		vote = Vote.objects.create(resource=resource,person=person,value=value)
	# redirect back to topic detail
	return redirect('TopicDetails',slug =  resource.topic.slug)


def test(request,slug):
	return HttpResponseRedirect(reverse("TopicDetails",kwargs={'slug':slug}))

def autocompleteSuggestionTopic(request):
	if request.is_ajax():
		queryset = Topic.objects.filter(title__icontains=request.GET.get('search', None))
		filter_topic = []        
		for i in queryset:
			filter_topic.append(i.title)
		data = {
			'list': filter_topic,
		}
		return JsonResponse(data)


url_entires = {}

'''
Below method is used to insert the data into model when url is apporved by the user. 
'''
def youtubeResource(request):
	if request.method == "POST":
		if request.POST.get("next") == "Yes":	
			items = url_entires['session_variable']

			contentDetails = items["contentDetails"]
			snippet = items['snippet']
			statistics = items['statistics']
			m,s = contentDetails["duration"].replace("PT","").replace("S","").split("M")
			dur = int(s) + int(m)*60 	
			result = {
				"published_at"	:	snippet["publishedAt"].replace("T"," ").replace("Z",""),
				"title"			:	snippet['title'],
				"description"	:	snippet['description'],
				"thumbnail_url"	:	snippet['thumbnails']['high']['url'],
				"duration"		:	dur,
				"view_count"	:	int(statistics['viewCount']),
				"like_count"	:	int(statistics['likeCount']),
				"dislike_count"	:	int(statistics['dislikeCount']),
				"comment_count"	:	int(statistics['commentCount'])
			}
			del url_entires['session_variable']
			resource = YoutubeResource(**result)
			resource.save()

		elif request.POST.get("no") == "No":
			pass
	return HttpResponseRedirect(reverse('youtubeResourcePreview'))

'''
Below method stores the data returned by the Youtube v3 API in a global variable "url_entries" 
according to the session of users as key and data as its value. This data is furthur used when
user approved the url.
'''
def youtubeResourcePreview(request):
	flag = False
	if request.method == "POST":
		url = request.POST.get("url")
		flag = True
		if "watch" in url:
			#Identifies that it is a video
			_,slug = url.split("watch?v=")
			try:
				contents = urlreq.urlopen("https://www.googleapis.com/youtube/v3/videos?part=snippet%2CcontentDetails%2Cstatistics&id="+slug+"&key="+YOUTUBE_API_KEY).read()
				contents = json.loads(contents.decode('utf-8')) 
				items = contents["items"][0]
				snippet = items['snippet']
	
				context = {
					"title"			:	snippet['title'],
					"thumbnail_url"	:	snippet['thumbnails']['standard']['url'],
					"flag"			: 	flag
				}
				url_entires['session_variable'] = items
				return render(request,'learn/youtube_resource.html',context)
			except Exception as e:
				print(e)
				return HttpResponse("Check console")

		elif "playlist" in url:
			#Identifies that it is a playlist
			pass
		elif "channel" in url:
			#Identifies that it is a channel
			pass
	return render(request,'learn/youtube_resource.html',{"flag":flag})