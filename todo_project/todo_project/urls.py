"""todo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from todo import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Home
    path('', views.HomeView.as_view(), name='home'),
    
    # Authentication
    path('signup/', views.SignUpView.as_view(), name='signupuser'),
    path('logout/', views.LogoutUserView.as_view(), name='logoutuser'),
    path('login/', views.LoginUserView.as_view(), name='loginuser'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    
    # Todos
    path('todo/', include('todo.urls')),

    # API
    path('api/todos/', views.TodoList.as_view(), name='todolist'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token),
]
