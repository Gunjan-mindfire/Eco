import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.defaulttags import register
from django.urls import reverse
from django.core import serializers
from userProfile.models import s3Images

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from userProfile.serializers import s3ImagesSerializer
from EcoMail import settings


# Create your views here.
def registerUser(request):
    context = {
        'poolId': settings.userPoolId,
        'clientId':settings.clientId
    }
    return render(request, 'register.html', context)

def login(request):
    context = {
        'poolId': settings.userPoolId,
        'clientId':settings.clientId
    }
    return render(request, 'login.html', context )

def schedule(request):
    context = {
        'poolId': settings.userPoolId,
        'clientId':settings.clientId
    }
    return render(request, 'schedule.html', context)

def profile(request):
    context = {
        'poolId': settings.userPoolId,
        'clientId':settings.clientId,
        'accessKeyId':settings.accessKeyId,
        'secretAccessKey':settings.secretAccessKey,
        'Bucket':settings.Bucket
    }
    return render(request, 'profile.html',context)

@register.filter()
def get_range(value):
    return range(1,value)

# def s3Create(request):
#     s3Record = s3Images()
#     s3Record.cognitoId = request.GET['cognitoId']
#     s3Record.save()

#     data = serializers.serialize('json', [s3Record,])

#     return HttpResponse(data, content_type="application/json")

# def s3Get(request):
#     s3 = s3Images.objects.filter(cognitoId__contains=request.GET['cognitoId'])
#     data = serializers.serialize('json', s3)
#     return HttpResponse(data, content_type="application/json")

# def s3Update(request):
#     s3Record = s3Images.objects.get(cognitoId__contains=request.GET['cognitoId'])
#     s3Record.cognitoId = request.GET['cognitoId']
#     s3Record.link = request.GET['link']
#     s3Record.save()
#     data = serializers.serialize('json', [s3Record,])
#     return HttpResponse(data, content_type="application/json")

class Image(APIView):
    def post(self, request):
        serializer = s3ImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        image = s3Images.objects.filter(cognitoId=request.GET['cognitoId'])
        serializer = s3ImagesSerializer(image, many=True)
        return Response(serializer.data)

    def put(self, request):
        try:
            snipets = s3Images.objects.get(cognitoId__contains=request.query_params.get('cognitoId'))
        except s3Images.DoesNotExist:
            return Response({'result': "Given cognito id doesn't Exists"}, status=status.HTTP_404_NOT_FOUND)
        print(snipets)
        snipets.link = request.query_params.get('link')
        snipets.save()
        serializer = s3ImagesSerializer(snipets, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


