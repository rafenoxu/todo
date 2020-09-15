from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, logout, authenticate

from django.utils import timezone

from django.views.generic import TemplateView, ListView, UpdateView, CreateView, DeleteView
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse, reverse_lazy

from django.http import HttpResponse, JsonResponse, Http404

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import TodoForm, UserForm, ProfileForm

from .models import Todo

from .serializers import TodoSerializer

from .permissions import IsOwner

# Create your views here.
class HomeView(TemplateView):
    template_name = 'todo/home.html'

# Authentication
class SignUpView(View):
    def get(self, request):
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})

    def post(self, request):
        userCreationForm = UserCreationForm(request.POST)
        if userCreationForm.is_valid():
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Form data not valid. Try again'})


class LoginUserView(View):
    def get(self, request):
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})

    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username or password incorrect'})
        else:
            login(request, user)
            return redirect('home')


class LogoutUserView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return redirect('home')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'todo/profile.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return render(request, 'todo/profile.html', {'user_form': user_form, 'profile_form': profile_form})
        else:
            return render(request, 'todo/profile.html', {'user_form': user_form, 'profile_form': profile_form, 'error': 'invalid form data'})


# Todos
class CreateTodoView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo/createtodo.html'
    fields = ['title', 'description', 'important']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('currenttodos')


class CurrentTodosView(LoginRequiredMixin, ListView):
    context_object_name = 'todos'
    template_name = 'todo/currenttodos.html'

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user, completion_date_time__isnull=True) 


class CompletedTodosView(LoginRequiredMixin, ListView):
    context_object_name = 'todos'
    template_name = 'todo/completedtodos.html'

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user, completion_date_time__isnull=False)


class TodoView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo/viewtodo.html'
    fields = ['title', 'description', 'completion_date_time', 'important']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('currenttodos')


class CompleteTodoView(LoginRequiredMixin, View):
    def post(self, request, pk):
        todo = get_object_or_404(Todo, pk=pk, owner=request.user)
        todo.completion_date_time = timezone.now()
        todo.save()
        return redirect('currenttodos')


class DeleteTodoView(LoginRequiredMixin, DeleteView):
    model = Todo
    success_url = reverse_lazy('currenttodos')

# API
class TodoList(generics.ListCreateAPIView):
    """
    List all todos, or create new
    """
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        return Todo.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
