from users.models import Profile


def access_profile(request):
    if request.user.is_authenticated:
        
        access_profiles =Profile.objects.get(name =request.user)
        followings = access_profiles.following.all()#queryset of all the accounts that i follow ...
        my_guys = Profile.objects.filter(name__in = followings)[:4]  
        other_users = Profile.objects.exclude(name__in =followings)[:4] 
        
        return {"access_profiles":access_profiles , "my_guys":my_guys , "other_users":other_users }
    else:
        return {}