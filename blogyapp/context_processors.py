from users.models import Profile
from blogyapp.models import Entry


def access_profile(request):
    if request.user.is_authenticated:
        
        logged_in_user_articles = Entry.objects.filter(profile__name=request.user)
        
        access_profiles =Profile.objects.get(name =request.user)
        followings = access_profiles.following.all()#queryset of all the accounts that i follow ...
        my_guys = Profile.objects.filter(name__in = followings)[:4]  
        other_users = Profile.objects.exclude(name__in =followings)[:4] 
        
        return {"access_profiles":access_profiles , "my_guys":my_guys , "other_users":other_users,"logged_in_user_articles":logged_in_user_articles}
    
    else:
        return {}
    """  
def profile_detail(request,profile_id):
    if request.user.is_authenticated:
        profile =Profile.objects.get(id=profile_id) #Profile of a specific user
        profile_posts = profile.profiles_posts()
        
        my_profile = Profile.objects.get(name =request.user)  
        followings = my_profile.following.all()
        return {"profile":profile, "followings":followings, "profile_posts":profile_posts}
    else:
        return {}
        
       """  

   