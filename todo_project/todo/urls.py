from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateTodoView.as_view(), name='createtodo'),
    path('current/', views.CurrentTodosView.as_view(), name='currenttodos'),
    path('completed/', views.CompletedTodosView.as_view(), name='completedtodos'),
    path('<int:pk>', views.TodoView.as_view(), name='viewtodo'),
    path('<int:pk>/complete', views.CompleteTodoView.as_view(), name='completetodo'),
    path('<int:pk>/delete', views.DeleteTodoView.as_view(), name='deletetodo'),
]
