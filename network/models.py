from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    body = models.CharField(max_length=256, blank=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    like = models.ManyToManyField(User, blank=True, related_name="like")
    
class Following(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")