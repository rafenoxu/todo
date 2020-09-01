from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Todo(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creation_date_time = models.DateTimeField(auto_now_add=True)
    completion_date_time = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
