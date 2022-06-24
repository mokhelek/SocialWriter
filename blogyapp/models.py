
from django.db import models
from django.contrib.auth.models import User 
from users.models import Profile

from tinymce.models import HTMLField

# Create your models here.
class Topic(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  #It is called owner!!
    #activity = models.ForeignKey(LogEntry, on_delete=models.CASCADE)  # summoning all the user action data saved in LogEntry model
    text = models.CharField(max_length=200)
    topic_description = models.CharField(max_length=80)
    date_added = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
         #Return a string representation of the model.
        return self.text

class Entry(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE) # field with Topic data ...!
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE , blank=True , null=True) # Entry attached to a specific profile
    thumbnail = models.ImageField(upload_to="images", blank=True , null=True)
    uploaded = models.BooleanField(default=False)
    entry_title = models.TextField()
    introduction = models.CharField(max_length=600)
    text = HTMLField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        #Return a string representation of the model."""
        return self.entry_title
    

class Comments(models.Model):
   
    profile = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE) 
    
    date_created = models.DateTimeField(auto_now=True)
    comment = models.CharField(max_length=200 ,null=True, blank=True )
    
    class Meta:
        
        verbose_name_plural = 'comments'

    
