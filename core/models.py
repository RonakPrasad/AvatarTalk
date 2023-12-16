from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from AvatarGeneration.utils import unique_slug_generator
# Create your models here.

class Avatars(models.Model):
    GENDER = [
        ('male', 'male'),
        ('female', 'female'),
    ]
    name  = models.CharField(max_length=200)
    gender = models.FileField(max_length=100, choices=GENDER)

    def __str__(self):
        return self.name
    
class Voices(models.Model):
    audio_file = models.FileField(max_length=100)
    audio_id  = models.CharField(max_length=200)
    audio_title = models.CharField(max_length=200)
    
    def __str__(self):
        return self.audio_id
    

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True,
                            blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.email
    
def slug_creator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_creator, sender=Project)

class ProjectProperties(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    avatar_data = models.ForeignKey(Avatars, on_delete=models.CASCADE, blank=True, null=True)
    driver_id = models.CharField(max_length=200, blank=True, null=True)
    presenter_id = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    audio_id = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f'{self.project.user.email} - {self.project.name}'

class ProjectVideo(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    video_file = models.FileField(max_length=500)
    
    def __str__(self):
        return self.video_file