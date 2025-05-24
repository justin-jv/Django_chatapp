from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    is_online = models.BooleanField(default=False)


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}: {self.message[:20]}'
    
class Group(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='group_memberships')

    def __str__(self):
        return self.name
    
class GroupMessage(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'[{self.group.name}] {self.sender}: {self.message[:20]}'
    
