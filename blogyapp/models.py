from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

# Create your models here.
class Topic(models.Model):
     #A topic the user is learning about.
    text = models.CharField(max_length=200)
    topic_description = models.CharField(max_length=80)
    date_added = models.DateTimeField(auto_now_add=True) 
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
         #Return a string representation of the model.
        return self.text

class Entry(models.Model):
    #Something specific learned about a topic."""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    entry_title = models.TextField()
    introduction = models.TextField(" make it catchy ")
    text = HTMLField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
        def __str__(self):
            #Return a string representation of the model."""
            return self.entry_title