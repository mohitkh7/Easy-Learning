from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import Sum
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from autoslug import AutoSlugField

# Fetching Admin for default values
# ADMIN=User.objects.get(username="admin")

# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_picture/",
        default="/profile_picture/default_profile_picture.png")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.name


# Categories class for categories of topics
class Category(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon_name = models.CharField(max_length=20, default="info")
    slug = AutoSlugField(populate_from="title", unique=True, editable=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'categories'


class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    # If a person deletes why is it happening ?
    person = models.ForeignKey('person', on_delete=models.SET('Anonymous'))
    category = models.ForeignKey(
        'category',
        on_delete=models.CASCADE,
        default=1)
    image = models.ImageField(upload_to="topic")
    views = models.IntegerField(default=0)
    slug = AutoSlugField(populate_from="title", unique=True, editable=True)
    added_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    # keyword

    def __str__(self):
        return self.title

    '''def save(self,*args,**kwargs):
		self.slug=slugify(self.title)
		super(Topic,self).save(*args,**kwargs)
	'''

    def get_absolute_url(self):
        return reverse("TopicDetails", args=[self.slug, ])


class Resource(models.Model):
    LEVELS = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advance', 'Advance'),
    )

    METHODS = (
        ('book', 'Book'),
        ('ebook', 'eBook'),
        ('video', 'Video'),
        ('website', 'Website'),
        ('blog', 'Blog'),
        ('mooc', 'MOOC'),
        ('other', 'Other'),
    )

    title = models.CharField(max_length=1000)
    description = models.TextField()
    person = models.ForeignKey('person', on_delete=models.SET('Anonymous'))
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    url = models.URLField()
    level = models.CharField(max_length=20, choices=LEVELS)
    language = models.CharField(max_length=30, default="English")
    method = models.CharField(max_length=20, choices=METHODS, null=True)
    score = models.IntegerField(default=0)  # based on vote
    price = models.FloatField()
    slug = AutoSlugField(populate_from="title", unique=True, editable=True)
    # time=models.CharField(max_length=100)
    added_on = models.DateTimeField(auto_now_add=True)
    # extra = models.CharField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("TopicDetails", args=[self.topic.slug, ])


class Review(models.Model):
    star = models.IntegerField()
    text = models.TextField()
    person = models.ForeignKey('person', on_delete=models.SET('Anonymous'))
    resource = models.ForeignKey('resource', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("TopicDetails", args=[self.resource.topic.slug, ])


class Bookmark(models.Model):
    person = models.ForeignKey('person', on_delete=models.SET('Anonymous'))
    resource = models.ForeignKey('resource', on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s " % (self.person, self.resource)


class Vote(models.Model):
    OPTION = (
        (1, "Upvote"),
        (0, "Undo"),
        (-1, "DownVote")
    )
    person = models.ForeignKey('person', on_delete=models.SET('Anonymous'))
    resource = models.ForeignKey('resource', on_delete=models.CASCADE)
    # 1 == Upvote -1 == Downvote
    value = models.IntegerField(default=1, choices=OPTION)

    def __str__(self):
        return "%s on %s by %s" % (self.value, self.resource, self.person)

# Signals to change in person field when user changes


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    p = Person.objects.get(user=instance)
    if instance.first_name:
        if instance.last_name:
            p.name = instance.first_name + " " + instance.last_name
        else:
            p.name = instance.first_name
    else:
        p.name = instance.username

    p.name = p.name.title()
    p.save()

# Signals to change resource score field when vote changes


'''
Picking all vote column for given resource than adding their value
'''


@receiver(post_save, sender=Vote)
def update_score_on_vote(sender, instance, **kwargs):
    '''
    all_vote_for_a_resource = Vote.objects.filter(resource=instance.resource)
    print(Vote.objects.filter(resource=instance.resource).aggregate(Sum('value')))
    ans = 0
    for vote in all_vote_for_a_resource:
            ans += vote.value
    instance.resource.score = ans
    instance.resource.save()

    '''
    sum_of_vote = Vote.objects.filter(
        resource=instance.resource).aggregate(
        Sum('value'))
    instance.resource.score = sum_of_vote['value__sum']
    instance.resource.save()


'''
Book => Author, Amazon Link, Free PDF, Pages, ISBN No., Publisher
Website => AlexaRank
Youtube Video => Channel, Views, Upvotes, Downvotes,
MOOC => Instructor,
'''
