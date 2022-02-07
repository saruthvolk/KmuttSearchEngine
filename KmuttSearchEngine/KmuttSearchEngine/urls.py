"""
Definition of urls for KmuttSearchEngine.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views
from django.conf.urls import include

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('upload_image/', views.upload_image),
    path('', views.home, name='home'),
    path('train_dict/', views.train_dict, name='train_dict'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('question/<id>', views.question, name='question'),
    path('admin/', views.Admin, name='admin'),
    path('admin/user', views.user, name='user'),
    path('profile', views.profile, name='profile'),
    path('admin/usermanagement/<operation>', views.usermanagement, name='usermanagement'),
    path('Crud_QA/<operation>/<id>', views.Crud_QA, name='Crud_QA'),
    path('about/', views.about, name='about'),
    path('login/',views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('database/', admin.site.urls),
    path('register/', views.register, name='register'),
]
