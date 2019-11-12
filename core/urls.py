from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('systems/<int:pk>/', views.SystemDetailView.as_view(), name='system-detail'),
#
    #path('users/', views.ProfileListView.as_view(), name='users'),
    #path('users/<str:username>/', views.ProfileDetailView.as_view(), name='user-messages'),
#
    #path('profile/<int:pk>/', views.ProfileDetailView.as_view(), name='profile'),
    #path('profile/update/<int:pk>', views.ProfileUpdateView.as_view(), name='profile-update'),
#
    #path('register/', views.RegisterView.as_view(), name='register'),
#
    #path('events/', views.EventListView.as_view(), name='events'),
    #path('events/new/', views.EventCreateView.as_view(), name='event-create'),
    #path('events/update/<int:pk>/', views.EventUpdateView.as_view(), name='event-update'),
    #path('events/delete/<int:pk>/', views.EventDeleteView.as_view(), name='event-delete'),
#
    #path('messages/', views.MessageListView.as_view(), name='messages'),
#
    #path('projects/', views.ProjectListView.as_view(), name='projects'),
    #path('projects/new/', views.ProjectCreateView.as_view(), name='project-create'),
    #path('projects/update/<int:pk>/', views.ProjectUpdateView.as_view(), name='project-update'),
    #path('projects/delete/<int:pk>/', views.ProjectDeleteView.as_view(), name='project-delete'),
    #path('about/', views.about, name='events-about'),
]

