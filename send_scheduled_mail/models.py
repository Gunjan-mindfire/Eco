from django.db import models

# Create your models here.
class scrapData(models.Model):
    link = models.TextField()
    title = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.title