from django.db import models

# Create your models here.
class s3Images(models.Model):
    cognitoId = models.CharField(max_length=255)
    link = models.TextField(default="/static/default.png")

    def __str__(self) -> str:
        return self.cognitoId