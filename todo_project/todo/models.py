from django.db import models
from django.db.models.signals import post_save

from django.contrib.auth.models import User

from django.dispatch import receiver

# Create your models here.

# Todo
class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date_time = models.DateTimeField(auto_now_add=True)
    completion_date_time = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    # To see it in admin as title
    def __str__(self):
        return self.title

# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField(blank=True)
