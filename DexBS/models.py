from django.db import models

# Create your models here.

class User(models.Model):
    rfid= models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=22)
    username=models.CharField(max_length=22)
    cake_day = models.DateField()
    desc = models.TextField()
    propic = models.CharField(max_length=10000)
    email = models.CharField(max_length=50)
    cover = models.CharField(max_length=7)
    def __str__(self):
        return f"{self.name}"
    
class Dex(models.Model):
    rfid= models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=22)
    desc = models.TextField()
    dex=models.CharField(max_length=22)
    cake_day = models.DateField()
    propic = models.ImageField(upload_to=f'd/dex_pics')
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    rules = models.TextField()
    rules_desc = models.TextField()
    cover = models.CharField(max_length=7)
    def __str__(self):
        return f"{self.name}"

class Post(models.Model):
    rfid = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dex = models.ForeignKey(Dex, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    cake_day = models.DateTimeField()
    file = models.FileField(upload_to=f'post/data/')
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
    upvote = models.IntegerField()
    downvote = models.IntegerField()
    def __str__(self):
        return f"{self.post.user.name} {self.content} {self.post.desc}"

class Membership(models.Model):
    dex = models.ForeignKey(Dex,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} --> {self.dex}"
    class Meta:
        unique_together = ('user','dex')




