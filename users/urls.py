from django.urls import path
from . import views

urlpatterns=[
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('profile/<str:pk>/send_message/', views.send_message, name='send_message'),
    path('account/', views.user_account, name='user_account'),
    path('account/edit/', views.edit_account, name='edit_account'),
    path('add_skill/', views.add_skill, name='add_skill'),
    path('update_skill/<str:pk>/', views.update_skill, name='update_skill'),
    path('delete_skill/<str:pk>/', views.delete_skill, name='delete_skill'),
    path('inbox/', views.inbox, name='inbox'),
    path('inbox/<str:pk>/', views.show_message, name='message'),

    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_user, name='logout_user'),
    path('regiser/', views.user_register, name='user_register')
]