from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    id=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    short_intro=models.CharField(max_length=200, null=True, blank=True, default='')
    bio=models.TextField(null=True, blank=True, default='')
    location=models.CharField(max_length=100, null=True, blank=True, default='')
    profile_image=models.ImageField(upload_to='profiles/', null=True, blank=True, 
		default='profiles/user-default.png')
    social_github=models.CharField(max_length=250, null=True, blank=True)
    social_twitter=models.CharField(max_length=250, null=True, blank=True)
    social_linkedin=models.CharField(max_length=250, null=True, blank=True)
    social_youtube=models.CharField(max_length=250, null=True, blank=True)
    social_website=models.CharField(max_length=250, null=True, blank=True)
    created=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=['created']
        indexes=[models.Index(fields=['id'])]


    def __str__(self) -> str:
        return self.user.username
    
    def full_name(self):
        return self.user.first_name + ' ' + self.user.last_name
    


class Skill(models.Model):
    id=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    owner=models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Message(models.Model):
    sender=models.ForeignKey(Profile, on_delete=models.CASCADE)
    recipient=models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='recipients')
    subject=models.CharField(max_length=100)
    body=models.TextField()
    is_read=models.BooleanField(default=False)
    id=models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.subject
    

    class Meta:
        ordering=['is_read','-created']
        indexes=[models.Index(fields=['id'])]