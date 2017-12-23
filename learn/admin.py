from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import *

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['title','description','icon_name','slug','is_active']
	ordering = ['title']

#For Topic Model Admin
class TopicAdmin(admin.ModelAdmin):
	list_display = ['title','description','category','views',]
	list_filter = ['category','is_active',]

class ResourceAdmin(admin.ModelAdmin):
	list_display = ['title','description','method','level','price','person']
	list_filter = ['level','method',]

class ReviewAdmin(admin.ModelAdmin):
	list_display = ['resource','star','text','person']

# Register your models here.
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Person)
admin.site.register(Topic,TopicAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Bookmark)
admin.site.register(Vote)
admin.site.register(LogEntry)
admin.site.register(Category,CategoryAdmin)

