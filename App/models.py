from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    bio = models.TextField(max_length=160, blank=True, null=True)
    useremail = models.EmailField()
    password = models.CharField(max_length=100)
    pimage = models.ImageField(upload_to='profiles/')
    
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=500, blank=True)
    likers = models.ManyToManyField(User, blank=True, related_name='likes') 
    savers = models.ManyToManyField(User,blank=True , related_name='saved')
    comment_count = models.IntegerField(default=0)
    

class PostMedia(models.Model):
    post = models.ForeignKey(Posts,blank=True, on_delete=models.CASCADE , related_name="media_post")
    media = models.ImageField(upload_to='posts/')
    
class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')