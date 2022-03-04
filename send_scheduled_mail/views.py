import json
from django.shortcuts import render
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.http import HttpResponseRedirect
from django.urls import reverse

import datetime

def schedule_mail(request):
    hours = request.POST['hour']
    minutes = request.POST['minute']
    email = request.POST['email']
    schedule, created = CrontabSchedule.objects.get_or_create(hour = hours, minute = minutes)
    task = PeriodicTask.objects.create(crontab = schedule, 
                                        name ="mailscheduled" + str(datetime.datetime.timestamp(datetime.datetime.now())),
                                        task='send_scheduled_mail.tasks.scrapnews',
                                        args=json.dumps([email])
                                        )
    return HttpResponseRedirect(reverse('userProfile:schedule'))
