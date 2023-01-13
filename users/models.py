
from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Profile(models.Model):
    name = models.OneToOneField(User, on_delete=models.CASCADE ,default=1 ) # this has the username inside
    bio = models.CharField(max_length=150,blank=True, default="Hey There I'm using SocialWriter ")
    avatar = models.ImageField(null=True, upload_to="blogyapp/images/profiles_img", default="default.jpg")
    following = models.ManyToManyField(User,related_name="following", blank=True)
    followers = models.IntegerField(default=0) 
    date_created = models.DateTimeField(auto_now=True)
    liked_articles = models.ManyToManyField("blogyapp.Entry",related_name="liked_articles", blank=True)
    bookmarked_articles = models.ManyToManyField("blogyapp.Entry",related_name="bookmarked_articles", blank=True)
    
    twitter_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    personal_link = models.URLField(blank=True, null=True)
    
    def profiles_posts(self):
        return self.entry_set.all()
 
    def __str__(self):
        return str(self.name.username)
 
