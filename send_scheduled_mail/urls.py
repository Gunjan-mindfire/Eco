from django.urls import path
from . import views

app_name = "send_scheduled_mail"

urlpatterns = [
    path('schedule_mail', views.schedule_mail, name="schedule_mail"),
]
