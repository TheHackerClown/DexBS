from django.db import models

# Create your models here.

class User(models.Model):
    rfid= models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=22)
    username=models.CharField(max_length=22)
    cake_day = models.DateField()
    propic = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.name}"
    
class Dex(models.Model):
    rfid= models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=22)
    desc = models.TextField()
    dex=models.CharField(max_length=22)
    cake_day = models.DateField()
    propic = models.ImageField(upload_to='static/dex_pics/')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    cover = models.ImageField(upload_to='static/covers/')
    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    rfid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dex = models.ForeignKey(Dex, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    file = models.FileField(upload_to='static/data/')
    upvote = models.IntegerField()
    downvote = models.IntegerField()
    def __str__(self):
        return f"{self.user.name} {self.desc}"

class Comment(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField()
    cake_day = models.DateTimeField()
    dex = models.ForeignKey(Dex,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    like = models.IntegerField()
    dislike = models.IntegerField()
    def __str__(self):
        return f"{self.post.user.name} {self.content} {self.post.desc}"

class Membership(models.Model):
    dex = models.ForeignKey(Dex,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} --> {self.dex}"
    class Meta:
        unique_together = ('user','dex')




