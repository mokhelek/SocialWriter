from ast import Not
from users.models import Profile
from blogyapp.models import Entry , Notification


def access_profile(request):
    if request.user.is_authenticated:
        
        notifications = Notification.objects.filter(entry__profile__name = request.user ).order_by("-date_created")
        
        logged_in_user_articles = Entry.objects.filter(profile__name=request.user)
        try:
            access_profiles =Profile.objects.get(name =request.user)
            followings = access_profiles.following.all() 
            my_guys = Profile.objects.filter(name__in = followings)[:4]  
            other_users = Profile.objects.exclude(name__in =followings)[:4] 
            
            
            return {"access_profiles":access_profiles ,
                    "my_guys":my_guys , 
                    "other_users":other_users,
                    "logged_in_user_articles":logged_in_user_articles,
                    "notifications": notifications ,
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
