
from users.models import Profile
from blogyapp.models import Entry , Notification
from django.db.models import Q

def access_profile(request):
    if request.user.is_authenticated:
        
        notifications = Notification.objects.filter( Q(entry__profile__name = request.user) | Q(profile__name = request.user) )
        
        
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
                    "notifications": notifications ,
                    }
               
    else:
        return {}
