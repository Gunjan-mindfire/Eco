from userProfile.models import s3Images
from rest_framework import serializers

class s3ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = s3Images
        fields = '__all__'