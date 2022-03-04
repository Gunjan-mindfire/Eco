from django.contrib import admin
from django.urls import path
from .views import *
from django.views.generic import TemplateView

app_name = "userProfile"

urlpatterns = [
    path('register/', registerUser, name='registerUser'),
    path('login/',login, name='login'),
    path('schedule-Mail/', schedule, name='schedule'),
    path('profile/', profile, name='profile'),
    # path('s3Create/', views.s3Create, name='s3Create'),
    # path('s3Get/', views.s3Get, name='s3Get'),
    # path('s3Update/', views.s3Update, name='s3Update'),
    path('s3Image/', Image.as_view(), name='Image'),
    path('', index, name='index'),
]
