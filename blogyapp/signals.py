
from django.db.models.signals import post_save, m2m_changed , post_delete
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


def delete_like_notification(sender, instance, **kwargs):
    
    Notification.objects.filter(profile = instance.profile , entry = instance.entry ).delete()
       
post_delete.connect(delete_like_notification, sender=Like )


def delete_bookmark_notification(sender, instance, **kwargs):
    
    Notification.objects.filter(profile = instance.profile , entry = instance.entry ).delete()
       
post_delete.connect(delete_bookmark_notification, sender=Bookmark )




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



def following_notification(sender, instance, action,*args, **kwargs):
    print("following signal : ",instance)
    if action == "post_add":
        Notification.objects.create( 
                                profile = instance,
                                message = f"{instance} started following you" ,
                                    )
    if action == "post_remove":
       Notification.objects.filter(message = f"{instance} started following you").delete()

m2m_changed.connect(following_notification, sender=Profile.following.through )



