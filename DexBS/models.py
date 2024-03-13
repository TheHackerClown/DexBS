from django.db import models

# Create your models here.

class User(models.Model):
    rfid= models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=22)
    username=models.CharField(max_length=22)
    cake_day = models.DateField()
    propic = models.ImageField(upload_to='static/profile_pics/')
    def __str__(self):
        return f"{self.name}"
    
class Dex(models.Model):
    rfid= models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=22)
    desc = models.CharField(max_length=50)
    dex=models.CharField(max_length=22)
    cake_day = models.DateField()
    propic = models.ImageField(upload_to='static/prodex_pics/')
    cover = models.ImageField(upload_to='static/covers/')
    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    rfid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dex = models.ForeignKey(Dex, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    file = models.FileField(upload_to='static/data/')

