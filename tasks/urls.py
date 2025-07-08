from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),
    path('update/<int:pk>/', views.task_update, name='task-update'),
    path('delete/<int:pk>/', views.task_delete, name='task-delete'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('superuser/dashboard/', views.superuser_dashboard, name='superuser_dashboard'),
    path('profile/', views.user_profile, name='user-profile'),
    path('update-task-order/', views.update_task_order, name='update-task-order'),
]