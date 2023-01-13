
from django.db.models.signals import post_save, pre_save , m2m_changed
from django.contrib.auth.models import User
from .models import *
from users.models import *

def comment_notification(sender, instance, created, **kwargs):

	if created:
		Notification.objects.create( 
            profile = instance.profile ,     
            entry = instance.entry,            
			message= instance.comment,
	
			)
post_save.connect(comment_notification, sender=Comments )




def like_notification(sender, instance, created,*args, **kwargs):
    if created :
        Notification.objects.create( 
                                profile = instance.profile,
                                entry = instance.entry ,
                                message = " liked your article -- test"
                                    )
        

post_save.connect(like_notification, sender=Like )

def bookmark_notification(sender, instance, created,*args, **kwargs):
    if created :
        Notification.objects.create( 
                                profile = instance.profile,
                                entry = instance.entry ,
                                message = " bookmarked your article -- test"
                                    )
        

post_save.connect(bookmark_notification, sender=Bookmark )

