from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(default = 'Insert Title Here', max_length = 50)
    by_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date = models.DateField(default = timezone.now)
    text = models.TextField(default = 'Insert Text Here')
    images = models.TextField(default = 'Insert Image Here', null = True, blank = True)
    likes = models.IntegerField(default = 0)
    dislikes = models.IntegerField(default = 0)