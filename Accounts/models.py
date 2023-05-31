from django.db import models

# Create your models here.

class Mail(models.Model):
    From = models.EmailField()
    To = models.EmailField()
    Subject = models.CharField(max_length=1000)
    Body = models.CharField(max_length=1000)
    Time_received = models.DateTimeField()