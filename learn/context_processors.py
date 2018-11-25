from .models import Category 
from .models import Topic
def categories_processor(request):
	categories = Category.objects.all()            
	return {'categories': categories}

def topics_processor(request):
	topics = Topics.objects.all()
	return {'topics':topics}