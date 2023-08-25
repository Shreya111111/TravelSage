from django.db import models

# Create your models here.
class profile(models.Model):
    name =models.CharField(max_length=100)
    email=models.EmailField()
    userdetails=models.CharField(max_length=1000)
    #img=models.ImageField(upload_to='pics')
    password=models.CharField(max_length=20)
    status=models.BooleanField()

