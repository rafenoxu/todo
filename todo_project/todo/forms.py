from django.forms import ModelForm

from .models import Todo
from .models import Profile

from django.contrib.auth.models import User

class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'important']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['about']
