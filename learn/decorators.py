'''
This file define custom decorators just like login_required
'''
from django.shortcuts import redirect
from functools import wraps

def strictly_no_login(function):
	@wraps(function)
	def wrap(request,*args,**kwargs):
		#redirecting to home page if already logged in 
		if request.user.is_authenticated:
			return redirect("TopicList")
		else:
			return function(request,*args,**kwargs)
#	wrap.__doc__ = function.__doc__
#	wrap.__name__ = function.__name__
	return wrap