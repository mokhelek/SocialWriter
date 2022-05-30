from django.db import models
from django.contrib.auth.models import User 

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
    thumbnail = models.ImageField(upload_to="images")
    uploaded = models.BooleanField(default=False)
    entry_title = models.TextField()
    introduction = models.TextField(" make it catchy ")
    text = HTMLField()
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        #Return a string representation of the model."""
        return self.entry_title