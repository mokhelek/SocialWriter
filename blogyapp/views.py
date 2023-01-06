
from django.shortcuts import render, redirect

from django.contrib.auth.models import User 
from .models import  Entry , Comments

from django.contrib.admin.models import LogEntry 
from .forms import EntryForm , CommentsForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

from users.models import Profile
from itertools import chain

from django.db.models import Q

# Create your views here.


def home1(request):

    if request.user.is_authenticated:
        
        followings_url = request.path
        print(followings_url)
        
        recommended_articles = Entry.objects.all() 
        my_profile =Profile.objects.get(name =request.user)  # profile of logged in user
        comments = Comments.objects.all()
        entries = Entry.objects.all().order_by("-date_added")
    
        followings = my_profile.following.all() #queryset of all the accounts that i follow ...
        my_guys = Profile.objects.filter(name__in = followings).exclude(Q(name=my_profile.name))[:6]  
        other_users = Profile.objects.exclude(name__in =followings).exclude(Q(name=my_profile.name))[:6] 
        
        
        context = { "entries":entries   ,
                   "followings":followings, 
                   "my_guys":my_guys ,
                   "other_users":other_users , 
                   "my_profile":my_profile,
                   "comments":comments, 
                   "recommended_articles":recommended_articles,
                   "followings_url":followings_url
                   }
        
        return render(request, 'blogyapp/landing_page.html',context)
    
    
    else:
            
        authors = Entry.objects.order_by("-popularity")
        top_authors = []
        
        for i in authors:
            if i.profile.name not in top_authors:
                top_authors.append(i.profile.name) 
        
        top_authors_details = Profile.objects.filter(name__in=top_authors)[:10]

        popular = Entry.objects.order_by("-popularity")[:4]
        
        return render(request, 'blogyapp/landing_page.html' , {"popular":popular,"top_authors_details":top_authors_details})


def following(request):

    if request.user.is_authenticated:
        
        followings_url = request.path
        print(followings_url)
        
        recommended_articles = Entry.objects.all() 
        my_profile =Profile.objects.get(name =request.user)  # profile of logged in user
        comments = Comments.objects.all()
        entries = []
        sorted_articles = None

        followings = my_profile.following.all() #queryset of all the accounts that i follow ...
        my_guys = Profile.objects.filter(name__in = followings).exclude(Q(name=my_profile.name))[:6]  
        other_users = Profile.objects.exclude(name__in =followings).exclude(Q(name=my_profile.name))[:6] 
        profiles = [name for name in followings]
        
        for i in profiles:
            if i != my_profile.name:
                p = Profile.objects.get(name=i)
                p_posts = p.entry_set.all()
                entries.append(p_posts)
            
        my_posts = my_profile.profiles_posts()
        entries.append(my_posts)    
        
        if len(entries)>0:
            sorted_articles = sorted(chain(*entries) , reverse = True , key = lambda obj: obj.date_added)
            
        
        context = { "entries":sorted_articles  ,
                   "followings":followings, 
                   "my_guys":my_guys ,
                   "other_users":other_users , 
                   "my_profile":my_profile,
                   "comments":comments, 
                   "recommended_articles":recommended_articles,
                   "followings_url":followings_url
                   }
        
        return render(request, 'blogyapp/landing_page.html',context)
    
    
    else:
            
        authors = Entry.objects.order_by("-popularity")
        top_authors = []
        
        for i in authors:
            if i.profile.name not in top_authors:
                top_authors.append(i.profile.name) 
        
        top_authors_details = Profile.objects.filter(name__in=top_authors)[:10]

        popular = Entry.objects.order_by("-popularity")[:4]
        
        return render(request, 'blogyapp/landing_page.html' , {"popular":popular,"top_authors_details":top_authors_details})





def popular(request):

    if request.user.is_authenticated:
      
        recommended_articles = Entry.objects.all() 
        my_profile =Profile.objects.get(name =request.user)  # profile of logged in user
        comments = Comments.objects.all()
        entries = Entry.objects.order_by("-popularity")
    
        followings = my_profile.following.all() #queryset of all the accounts that i follow ...
        my_guys = Profile.objects.filter(name__in = followings).exclude(Q(name=my_profile.name))[:6]  
        other_users = Profile.objects.exclude(name__in =followings).exclude(Q(name=my_profile.name))[:6] 
        
        
        context = { "entries":entries   ,
                   "followings":followings, 
                   "my_guys":my_guys ,
                   "other_users":other_users , 
                   "my_profile":my_profile,
                   "comments":comments, 
                   "recommended_articles":recommended_articles,
                   
                   }
        
        return render(request, 'blogyapp/landing_page.html',context)
    
    
    else:
            
        authors = Entry.objects.order_by("-popularity")
        top_authors = []
        
        for i in authors:
            if i.profile.name not in top_authors:
                top_authors.append(i.profile.name) 
        
        top_authors_details = Profile.objects.filter(name__in=top_authors)[:10]

        popular = Entry.objects.order_by("-popularity")
        
        return render(request, 'blogyapp/landing_page.html' , {"popular":popular,"top_authors_details":top_authors_details})




@login_required
def new_entry(request, profile_id ):
    profile_for_article = Profile.objects.get(id=profile_id)
    
    profile = Profile.objects.get(name =request.user)  # current logged in user profile

    if request.method != 'POST':
        form = EntryForm()
    else:  # the form is  submited
        form = EntryForm(request.POST , request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.profile_for_article = profile_for_article
            new_entry.profile = profile
            new_entry.save()
            get_id = form.instance.id   # here we are getting the unique id of a specific entry !!
            print(get_id)
      
            entry = Entry.objects.get(id=get_id)
            if 'upload' in request.POST:

                entry.uploaded = True  # please note
                entry.save(update_fields=['uploaded'])

            # WHAT IN THE WORLD IS GOING ON HERE!!!
            return redirect('blogyapp:home1' )
    context = {'profile_id': profile_id, 'form': form, "profile":profile}
    return render(request, 'blogyapp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogyapp:home1'  )

    context = {'entry': entry, 'form': form}
    return render(request, 'blogyapp/edit_entry.html', context)


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
   
    entry.delete()
    return redirect('blogyapp:home1' )


def read(request, read_id):
    if request.user.is_authenticated:
        
        my_profile = Profile.objects.get(name =request.user)  
        followings = my_profile.following.all()
        entry = Entry.objects.get(id=read_id) 
        comments = Comments.objects.filter( entry = entry)  # showing only the comments of a specific entry post
     
        #profile_login_user = Profile.objects.get(name = request.user) 
        
        #commenter = profile_login_user  #profile of logged in user
        popularity = entry.popularity
        
        if request.method != 'POST':
            form = CommentsForm()
        else:
            
            
            form = CommentsForm(data=request.POST)
            if form.is_valid():
                #form.profile_login_user = profile_login_user 
                new_comment = form.save(commit=False)
                popularity = popularity + 1
                entry.popularity = popularity
                new_comment.entry = entry 
                # first variable is the actual field from the model that you want to attach to ...
                # the second variable is the queryset or varible that you update with
                # in simple  terms this is a " from " & "to"
                new_comment.profile = Profile.objects.get(name = request.user) 
                entry.save(update_fields=["popularity"])
                new_comment.save()
                return redirect('blogyapp:read', read_id= entry.id)
        
        context = {"entry": entry, "form":form  ,"comments":comments , "followings":followings}
        return render(request, "blogyapp/read.html", context)
    else:
        entry = Entry.objects.get(id=read_id) 
        comments = Comments.objects.filter( entry = entry)  # showing only the comments of a specific entry post
       
        
        popularity = entry.popularity
        
        if request.method != 'POST':
            form = CommentsForm()
        else:
            
            
            form = CommentsForm(data=request.POST)
            if form.is_valid():
                #form.profile_login_user = profile_login_user 
                new_comment = form.save(commit=False)
                popularity = popularity + 1
                entry.popularity = popularity
                new_comment.entry = entry 
                # first variable is the actual field from the model that you want to attach to ...
                # the second variable is the queryset or varible that you update with
                # in simple  terms this is a " from " & "to"
                new_comment.profile = Profile.objects.get(name = request.user) 
                entry.save(update_fields=["popularity"])
                new_comment.save()
                return redirect('blogyapp:read', read_id= entry.id)
        
        context = {"entry": entry, "form":form ,"comments":comments }
        return render(request, "blogyapp/read.html", context)
        

def practice(request):
    profiles = Profile.objects.all()
    context = {"profiles":profiles}
    return render(request , "blogyapp/practice.html" , context)

def profile_detail(request,profile_id):
    profile =Profile.objects.get(id=profile_id) #Profile of a specific user
    profile_posts = profile.profiles_posts()
    
    my_profile = Profile.objects.get(name =request.user)  
    followings = my_profile.following.all()


    context ={"profile":profile, "followings":followings, "profile_posts":profile_posts}
    return render(request , "blogyapp/profile_detail.html" , context )

def follow_unfollow(request,profile_id):
    profile =Profile.objects.get(id=profile_id)
    followers = profile.followers
    
    if request.method == 'POST':
        my_profile =Profile.objects.get(name =request.user)  
        followings = my_profile.following.all()
        
        if profile.name in followings: # if i am following this guy
            my_profile.following.remove(profile.name)
            followers = followers - 1
            profile.followers = followers
            profile.save(update_fields=["followers"])
            
            my_profile.save()
        else:
            my_profile.following.add(profile.name)
            followers = followers + 1
            print(followers)
            profile.followers = followers
            profile.save(update_fields=["followers"])
            
            my_profile.save()
            
        
        return redirect('blogyapp:profile_detail', profile_id = profile.id)

    return render(request , "blogyapp/profile_detail.html" )

def like_unlike(request, entry_id):
    current_link = request.path    
    entry = Entry.objects.get(id = entry_id)
    profile = Profile.objects.get(name = request.user)
    liked_articles = profile.liked_articles.all()
    number_of_likes = entry.likes
    popularity = entry.popularity

    if request.method == 'POST':
        
        if entry in liked_articles:
            profile.liked_articles.remove(entry)
            number_of_likes = number_of_likes - 1
            popularity = popularity - 1
            entry.popularity = popularity
            entry.likes = number_of_likes
            
            entry.save(update_fields=["likes","popularity"])
            entry.save()
            profile.save()
            
        else:
            profile.liked_articles.add(entry)
            number_of_likes = number_of_likes + 1
            popularity = popularity + 1
            entry.popularity = popularity
            entry.likes = number_of_likes
            
            entry.save(update_fields=["likes","popularity"])
            entry.save()
            profile.save()
        
        if current_link == f"/like_unlike/{entry_id}/" :
            return redirect('blogyapp:home1')
        else:
            return redirect('blogyapp:read', entry_id )

def bookmark(request,entry_id):
    current_link = request.path   
    entry = Entry.objects.get(id = entry_id)
    bookmarks  = entry.bookmarks  # int value of bookmarks
    
    my_profile =Profile.objects.get(name = request.user)
    
    popularity = entry.popularity
    
    bookmarked_articles = my_profile.bookmarked_articles.all()
    if request.method == 'POST':
        if entry in bookmarked_articles: 
            my_profile.bookmarked_articles.remove(entry)
            
            bookmarks = bookmarks - 1
            popularity = popularity - 1
            entry.popularity = popularity
            
            entry.bookmarks = bookmarks
            
            entry.save(update_fields=["bookmarks","popularity"])
            
            my_profile.save()
        else:
            my_profile.bookmarked_articles.add(entry)
            
            bookmarks = bookmarks + 1
            popularity = popularity + 1
            entry.popularity = popularity
            
            entry.bookmarks = bookmarks
            
            entry.save(update_fields=["bookmarks","popularity"])
            
            my_profile.save()
            
        
        if current_link == f"/bookmark/{entry_id}/" :
            return redirect('blogyapp:home1')
        else:
            return redirect('blogyapp:read', entry_id )
    
def my_bookmarks(request, profile_id):
    
    return render(request,"blogyapp/bookmarks.html")

def user_entries(request):
    
    return render(request,"blogyapp/user_entries.html")

def publish_or_unpublish(request , entry_id):
    entry = Entry.objects.get(id = entry_id)
    
    profile_for_article = entry.profile
    
 
    entries = entry.order_by('-date_added') 
    uploaded = entry.uploaded
    print(uploaded)
    
    if uploaded is True:
        uploaded = False
        entry.uploaded = uploaded
        entry.save(update_fields=['uploaded'])
        entry.save()
   
        return redirect("blogyapp:index" )
        
    if uploaded is False:
        uploaded = True
        entry.uploaded = uploaded
        entry.save(update_fields=['uploaded'])
        entry.save()
      
        return redirect("blogyapp:index" )
    
    
    return render(request, 'blogyapp/articles.html', {"entries":entries})
        
      
    
    
