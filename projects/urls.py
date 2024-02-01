from django.urls import path

from . import views

urlpatterns=[
    path('', views.projects, name='projects'),
    path('projects/<str:pk>/', views.project, name='project'),
    path('projects/<str:pk>/delete/', views.delete_project, name='delete_project'),
    path('projects/<str:pk>/update/', views.update_project, name='update_project'),
    path('create_project/', views.create_project, name='create_project'),
]