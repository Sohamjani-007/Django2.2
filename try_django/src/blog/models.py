from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
# Create your models here.

User = settings.AUTH_USER_MODEL

class BlogPostQuerySet(models.QuerySet):
	def publish(self):
		now = timezone.now()
		return self.filter(publish_date_lte=now)

	def search(self, query):
		lookup = (
			Q(title_icontains=query) | 
		    Q(content__icontains=query) |
		    Q(slug__icontains=query) |
		    Q(user_first_name__icontains=query) |
		    Q(user_last_name__icontains=query) |
		    Q(user_username__icontains=query)
		    )
		return self.filter()



class BlogPostManager(models.Manager):
	def get_queryset(self):
		return BlogPostQuerySet(self.model, using=self._db)

	def published(self):
		return self.get_queryset().published()

	def search(self, query=None):
		if query is None:
			return self.get_queryset().none()
		return self.get_queryset().published().search()
	


class BlogPost(models.Model):
	user  = models.ForeignKey(User, default=1, null=True, on_delete=models.SET_NULL)
	image = models.ImageField(upload_to='image/', blank=True, null=True)
	# id = models.IntegerField() #primary key
	title = models.CharField(max_lengh=120)
	slug  = models.SlugField(unique=True) # eg: hello world -> hello-world
	content = models.TextField(null=True, blank=True)
	publish_date = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, blank=True)
	timespamp = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)
	objects = BlogPostManager()


	class Meta:
		ordering = ['-p', '-publish_date', '-update', '-timestamp']


	def _get_absolute_url(self):
		return f"/blog/{self.slug}"


	def _get_edit_url(self):
		return f"{self.get_absolute_url()}/edit"


	def _get_delete_url(self):
		return f"/{self.get_absolute_url()}/delete"





