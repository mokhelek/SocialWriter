
from django.db import models
from django.contrib.auth.models import User 


# Create your models here.
class Profile(models.Model):
    #name = models.OneToOneField(User, on_delete=models.CASCADE ) # this has the username inside
    bio = models.CharField(max_length=300,blank=True, default="Hey There I'm using Bloggy")
    avatar = models.ImageField(null=True, upload_to="images", default="default.png")
    
    following = models.ManyToManyField(User,related_name="following", blank=True)
    
    followers = models.IntegerField(default=0)
    
    date_created = models.DateField(auto_now=True)
    
    def profiles_posts(self):
        return self.entry_set.all()
    
    def __str__(self):
        return str(self.name.username)
