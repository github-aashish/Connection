from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now, null=True)
    bio = models.TextField(max_length=160, blank=True, null=True)
    useremail = models.EmailField()
    password = models.CharField(max_length=100)
    pimage = models.ImageField(upload_to='profiles/')
    backupimage = models.ImageField(upload_to='searches/', null=True)
    
    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profile_pic": self.pimage.url,
            "first_name": self.firstname,
            "last_name": self.lastname
        }
    def __str__(self):
        return self.username
    
class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateTimeField(default=timezone.now)
    content = models.TextField(max_length=500, blank=True)
    likers = models.ManyToManyField(User, blank=True, related_name='likes') 
    savers = models.ManyToManyField(User,blank=True , related_name='saved')
    comment_count = models.IntegerField(default=0)
    

class PostMedia(models.Model):
    post = models.ForeignKey(Posts,blank=True, on_delete=models.CASCADE , related_name="media_post")
    media = models.FileField(upload_to='posts/')
    
    @property
    def is_image(self):
        return self.media.name.endswith(('.png', '.jpg', '.jpeg', '.gif'))

    @property
    def is_video(self):
        return self.media.name.endswith(('.mp4', '.mov', '.avi', '.mkv'))
    
class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='commenters')
    comment_content = models.TextField(max_length=90)
    comment_time = models.DateTimeField(default=timezone.now)
    
    def serialize(self):
        return {
            "id": self.id,
            "commenter": self.commenter.serialize(),
            "body": self.comment_content,
            "timestamp": self.comment_time.strftime("%b %d %Y, %I:%M %p")
            }

class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User, blank=True, related_name='following')
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usernotification')
    status = models.BooleanField(default=False)

class NotificationMsgs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usermsgs')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='fromuser',null=True)
    for_post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='forpost',null=True)
    msg = models.CharField(max_length=500)
    msg_date = models.DateTimeField(default=timezone.now, null=True)
    
class ChatList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chatuser')
    chatUsers = models.ManyToManyField(User,blank=True, related_name='userchats')
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.message[:20]}"