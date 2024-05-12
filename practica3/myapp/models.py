from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)  # For simplicity
    email = models.EmailField()
    choice = models.CharField(max_length=50)  #'mathematician' or 'physicist'

    class Meta:
        app_label = 'myapp'