
from blogyapp.views import notifications
from users.models import Profile
from blogyapp.models import Entry , Notification
from django.db.models import Q

def access_profile(request):
    if request.user.is_authenticated:
        
        notifications = Notification.objects.filter( Q(entry__profile__name = request.user) | Q(profile__name = request.user) ).filter(notification_viewed = False )
        
        
        logged_in_user_articles = Entry.objects.filter(profile__name=request.user)
        try:
           
            #notifications = Notification.objects.filter(entry__profile__name = request.user)
            access_profiles =Profile.objects.get(name =request.user)
            followings = access_profiles.following.all() 
            my_guys = Profile.objects.filter(name__in = followings)[:4]  
            other_users = Profile.objects.exclude(name__in =followings)[:4] 
            return {"access_profiles":access_profiles ,
                    "my_guys":my_guys , 
                    "other_users":other_users,
                    "logged_in_user_articles":logged_in_user_articles,
                    "all_notifications": notifications ,
               
                    }
        except:
            
            access_profiles = ""
            followings = ""
            my_guys = ""  
            other_users = ""
            notifications = "nothing ?" 
            return {"access_profiles":access_profiles ,
                    "my_guys":my_guys , 
                    "other_users":other_users,
                    "logged_in_user_articles":logged_in_user_articles ,
                    "all_notifications": notifications ,
                    }
               
    else:
        return {}

def process_notifications(request):
    try:
        notifications_url = request.META["HTTP_REFERER"]
        
        notifications = Notification.objects.filter( Q(entry__profile__name = request.user) | Q(profile__name = request.user) )
        
        if notifications_url == "http://127.0.0.1:8000/notifications/" or notifications_url == "http://socialwriter.pythonanywhere.com/notifications/" or notifications_url == "https://socialwriter.pythonanywhere.com/notifications/":
            for i in notifications:
                if i.notification_viewed == False:
                    i.notification_viewed = True
                    i.save(update_fields=["notification_viewed"])
                    i.save()
        return {}
            
    except:
        return {}
        
        
