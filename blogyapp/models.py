
from django.db import models
from django.contrib.auth.models import User 
from users.models import Profile

from tinymce.models import HTMLField

# Create your models here.

class Entry(models.Model):

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE , blank=True , null=True) # Entry attached to a specific profile
    thumbnail = models.ImageField(upload_to="blogyapp/images/articles_img", blank=True , null=True)
    uploaded = models.BooleanField(default=False)
    entry_title = models.TextField()
    introduction = models.TextField()
    text = HTMLField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    popularity = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)  # number of likes for each Article
    bookmarks = models.IntegerField(default=0)  # number of bookmarks for each Article ... 
    
    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        #Return a string representation of the model."""
        return self.entry_title
    

class Comments(models.Model):
   
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE,related_name="entry" ) 
    
    date_created = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=200 ,null=True, blank=True )
    
    class Meta:
        
        verbose_name_plural = 'comments'

    
