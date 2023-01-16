
from django.db.models.signals import post_save, m2m_changed , post_delete
from django.contrib.auth.models import User
from .models import *
from users.models import *

def comment_notification(sender, instance, created, **kwargs):

	if created:
		Notification.objects.create( 
            reactor_profile = instance.profile ,     
            entry = instance.entry,            
			message= instance.comment,
            type = "comment",
			)
post_save.connect(comment_notification, sender=Comments )


def delete_like_notification(sender, instance, **kwargs):
    
    Notification.objects.filter(reactor_profile = instance.profile , entry = instance.entry ).delete()
       
post_delete.connect(delete_like_notification, sender=Like )


def delete_bookmark_notification(sender, instance, **kwargs):
    
    Notification.objects.filter(reactor_profile = instance.profile , entry = instance.entry ).delete()
       
post_delete.connect(delete_bookmark_notification, sender=Bookmark )




def like_notification(sender, instance, created,*args, **kwargs):
    if created :
        Notification.objects.create( 
                                reactor_profile = instance.profile,
                                entry = instance.entry ,
                                message =  f"{instance.profile} liked your article ",
                                type = "like",
                                    )
        

post_save.connect(like_notification, sender=Like )

def bookmark_notification(sender, instance, created,*args, **kwargs):
    if created :
        Notification.objects.create( 
                                reactor_profile = instance.profile,
                                entry = instance.entry ,
                                message = f"{instance.profile} bookmarked your article ",
                                type = "bookmark"
                                    )
        

post_save.connect(bookmark_notification, sender=Bookmark )



def following_notification(sender, instance, action,pk_set ,*args, **kwargs):

    if action == "post_add":
        user_id = []
        for i in pk_set:
            user_id.append(i)
   
        print( instance.following.get(id = user_id[0] ) )
        profiles = Profile.objects.get(name = instance.following.get(id = user_id[0] ) )
        Notification.objects.create( 
                                reactor_profile = instance, # the follower
                                message = f"{instance} started following you" ,
                                profile = profiles ,  # the  followed
                                type = "follow"
                                    )
    if action == "pre_remove":
 
        user_id = []
        for i in pk_set:
            user_id.append(i)

        print(user_id[0])
      
        profiles = Profile.objects.get(name = instance.following.get(id = user_id[0] ) )
        
        Notification.objects.filter(profile = profiles , reactor_profile = instance ).delete()

            

m2m_changed.connect(following_notification, sender=Profile.following.through )



