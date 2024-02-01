from uuid import uuid4
from django.db import models
from users.models import Profile


class Project(models.Model):
    id=models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    owner=models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    title=models.CharField(max_length=200)
    description=models.TextField(null=True, blank=True)
    demo_link=models.CharField(max_length=200, null=True, blank=True)
    featured_image=models.ImageField(null=True, blank=True, default='default.jpg')
    source_link=models.CharField(max_length=250, null=True, blank=True)
    vote_total=models.IntegerField(default=0, null=True, blank=True)
    vote_ratio=models.IntegerField(default=0, null=True, blank=True)
    tags=models.ManyToManyField('Tag', blank=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    
    
    class Meta:
        ordering=['-vote_ratio','-vote_total','title']
    

    @property
    def getVoteCount(self):
        reviews=self.review_set.all()
        total_vote=reviews.count()
        self.vote_total=total_vote + 1
        self.vote_ratio=reviews.filter(value='up').count()
        self.save()
    

class Review(models.Model):
    vote_type=[
        ('up','Up Vote'),
        ('down','Down Vote')
    ]
    owner=models.ForeignKey(Profile, on_delete=models.CASCADE)
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    body=models.TextField()
    value=models.CharField(max_length=100, choices=vote_type)
    id=models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    created=models.DateTimeField(auto_now_add=True)


    class Meta:
        unique_together=[['owner','project']]


    def __str__(self) -> str:
        return self.project.title



class Tag(models.Model):
    id=models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    name=models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.name
