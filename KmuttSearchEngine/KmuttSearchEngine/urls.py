"""
Definition of urls for KmuttSearchEngine.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views
from app import forms, views
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns

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
    path('profile/<operation>', views.profile, name='profile'),
    path('admin/usermanagement/<operation>', views.usermanagement, name='usermanagement'),
    path('Crud_QA/<operation>/<id>', views.Crud_QA, name='Crud_QA'),
    path('about/', views.about, name='about'),
    path('login/',views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('database/', admin.site.urls),
    path('register/', views.register, name='register'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),
]

urlpatterns += i18n_patterns (
    path('tinymce/', include('tinymce.urls')),
    path('upload_image/', views.upload_image),
    path('', views.home, name='home'),
    path('train_dict/', views.train_dict, name='train_dict'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('question/<id>', views.question, name='question'),
    path('admin/', views.Admin, name='admin'),
    path('admin/user', views.user, name='user'),
    path('profile/<operation>', views.profile, name='profile'),
    path('admin/usermanagement/<operation>', views.usermanagement, name='usermanagement'),
    path('Crud_QA/<operation>/<id>', views.Crud_QA, name='Crud_QA'),
    path('about/', views.about, name='about'),
    path('login/',views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),
    path('database/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('request/<operation>', views.requestmanagement, name='request'),

    path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), 
        name="password_reset_complete"),
)