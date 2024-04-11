from .views import *
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from rest_apis.viewsets.task_view import TaskViewSet
from rest_apis.viewsets.reminder_view import ReminderViewSet
from rest_apis.viewsets.activity_view import ActivityView

task_router = DefaultRouter()
task_router.register(r'task', TaskViewSet, basename='task')

reminder_router = DefaultRouter()
reminder_router.register(r'reminder', ReminderViewSet, basename='reminder')

activity_router = DefaultRouter()
activity_router.register(r'activity', ActivityView, basename='activity')

urlpatterns = [
    path('', index, name='index'),
    path('v1/api/register', RegisterAPI.as_view(), name='register'),
    path('v1/api/login', LoginAPI.as_view(), name='login'),
    path('v1/api/logout', LogOutAPI.as_view(), name='logout'),
    path('v1/api/profile', UpdateProfile.as_view(), name='profile'),
    path('v1/api/profile_image', UpdateProfileImage.as_view(), name='profile_image'),
    re_path(r'^api/v1/', include(task_router.urls)),
    re_path(r'^api/v1/', include(reminder_router.urls)),
    re_path(r'^api/v1/', include(activity_router.urls)),
    path('v1/api/recomandation', RecomendationView.as_view({'get': 'list'}), name='recomendation'),
]