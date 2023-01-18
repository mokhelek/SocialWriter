
from xml.etree.ElementTree import Comment
from django.shortcuts import render, redirect

from django.contrib.auth.models import User 
from .models import  Entry , Comments , Like ,Bookmark, Notification

from django.contrib.admin.models import LogEntry 
from .forms import EntryForm , CommentsForm , ProfileForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

from users.models import Profile
from itertools import chain

from django.db.models import Q

# Create your views here.


def home1(request):

    if request.user.is_authenticated:
        
        followings_url = request.path
        
        recommended_articles = Entry.objects.all() 
        my_profile =Profile.objects.get(name =request.user)  # profile of logged in user
        comments = Comments.objects.all()
        entries = Entry.objects.all().order_by("-date_added")
    
        followings = my_profile.following.all() #queryset of all the accounts that i follow ...
        my_guys = Profile.objects.filter(name__in = followings).exclude(Q(name=my_profile.name))[:6]  
        other_users = Profile.objects.exclude(name__in =followings).exclude(Q(name=my_profile.name))[:6] 
        
        
        context = { "entries":entries ,
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
    print(  "following : " +  request.path)
    if request.user.is_authenticated:
        
        followings_url = request.path

        
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
    #print(  "popular : "  ,  request.path)
    
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

def searched_articles(request):

    if request.user.is_authenticated:
        search_url = request.path
        form = request.POST
        search_text = request.POST.get("search_text")
        print(search_text)
        searched_articles = Entry.objects.filter(entry_title__contains = search_text ).order_by("-date_added") 
        
        my_profile =Profile.objects.get(name =request.user)  
        comments = Comments.objects.all()
        entries = Entry.objects.all().order_by("-date_added")
    
        followings = my_profile.following.all()
        my_guys = Profile.objects.filter(name__in = followings).exclude(Q(name=my_profile.name))[:6]  
        other_users = Profile.objects.exclude(name__in =followings).exclude(Q(name=my_profile.name))[:6] 
        
        
        context = { "entries":searched_articles,
                   "followings":followings, 
                   "my_guys":my_guys ,
                   "other_users":other_users , 
                   "my_profile":my_profile,
                   "comments":comments, 
                   "recommended_articles":searched_articles,
                    "search_url":search_url,
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


def edit_profile(request, profile_id):
    profile = Profile.objects.get(id = profile_id)
    if request.method != 'POST' :
        form = ProfileForm(instance = profile)
    else:
        form = ProfileForm(request.POST, request.FILES ,instance = profile )
        if form.is_valid():
            form.save()
            return redirect('blogyapp:profile_detail', profile_id )
            
    context = {"form":form,
               "profile":profile}
    return render(request, 'blogyapp/edit_profile.html', context )

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
        comments = Comments.objects.filter( entry = entry).order_by("-date_created")
    
        popularity = entry.popularity
        
        if request.method != 'POST':
            form = CommentsForm()
        else:
            
            
            form = CommentsForm(data=request.POST)
            if form.is_valid():
              
                new_comment = form.save(commit=False)
                popularity = popularity + 1
                entry.popularity = popularity
                new_comment.entry = entry 
               
                new_comment.profile = Profile.objects.get(name = request.user) 
                entry.save(update_fields=["popularity"])
                new_comment.save()
                return redirect('blogyapp:read', read_id= entry.id)
        
        context = {"entry": entry,
                   "form":form  ,
                   "comments":comments ,
                   "followings":followings,
                   "my_profile":my_profile}
        
        return render(request, "blogyapp/read.html", context)
    else:
        entry = Entry.objects.get(id=read_id) 
        comments = Comments.objects.filter( entry = entry)  
       
        
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
        

def profile_detail(request,profile_id):
    profile =Profile.objects.get(id=profile_id) #Profile of a specific user
    profile_comments = Comments.objects.filter(profile = profile).order_by("-date_created")

    profile_posts = profile.profiles_posts()
    
    my_profile = Profile.objects.get(name =request.user)  
    followings = my_profile.following.all()  # people that the logged in user follows

    context ={"profile":profile,
              "followings":followings,
              "profile_posts":profile_posts,
              "profile_comments":profile_comments,
              "my_profile":my_profile,
              }
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


def like_unlike(request,entry_id):
    previous_url = request.META["HTTP_REFERER"]  

    profile = Profile.objects.get(name = request.user)
    article = Entry.objects.get(id = entry_id )
    number_of_likes = article.likes
    liked = Like.objects.filter(profile = profile, entry = article).exists() 
    popularity = article.popularity
    
    if liked:
        Like.objects.filter(profile = profile, entry = article).delete()
        profile.liked_articles.remove(article)
        number_of_likes = number_of_likes - 1
        popularity = popularity - 1
        article.popularity = popularity
        article.likes = number_of_likes
        article.save(update_fields=["likes","popularity"])
        article.save()
        profile.save()
        
        
    else:
        Like.objects.create( profile = profile , entry = article )
        profile.liked_articles.add(article)
        number_of_likes = number_of_likes + 1
        popularity = popularity + 1
        article.popularity = popularity
        article.likes = number_of_likes
        article.save(update_fields=["likes","popularity"])
        article.save()
        profile.save()
        

    return redirect(previous_url + "#" + str(entry_id))
    

def bookmark(request,entry_id):
    previous_url = request.META["HTTP_REFERER"]  # url of previous page
    
    profile = Profile.objects.get(name = request.user)
    article = Entry.objects.get(id = entry_id )
    number_of_bookmarks = article.bookmarks
    bookmarked = Bookmark.objects.filter(profile = profile, entry = article).exists() 
    popularity = article.popularity
    
    if bookmarked:
        Bookmark.objects.filter(profile = profile, entry = article).delete()
        profile.bookmarked_articles.remove(article)
        number_of_bookmarks = number_of_bookmarks - 1
        popularity = popularity - 1
        article.popularity = popularity
        article.bookmarks = number_of_bookmarks
        article.save(update_fields=["bookmarks","popularity"])
        article.save()
        profile.save()
        
        
    else:
        Bookmark.objects.create( profile = profile , entry = article )
        profile.bookmarked_articles.add(article)
        number_of_bookmarks = number_of_bookmarks + 1
        popularity = popularity + 1
        article.popularity = popularity
        article.bookmarks = number_of_bookmarks
        article.save(update_fields=["bookmarks","popularity"])
        article.save()
        profile.save()
        
    return redirect( previous_url + "#" + str(entry_id) )
            
        
    """if current_link == f"/bookmark/{entry_id}/" :
            return redirect('blogyapp:home1')
        else:
            return redirect('blogyapp:read', entry_id )"""
    
def my_bookmarks(request, profile_id):
    my_profile =Profile.objects.get(name =request.user)
    entries = my_profile.bookmarked_articles.all()
    context = {"entries":entries,"my_profile":my_profile }
    return render(request,"blogyapp/bookmarks.html",context )

def user_entries(request):
    my_profile =Profile.objects.get(name =request.user)
    entries = Entry.objects.filter(profile = my_profile ).order_by("-date_added")
    
    form = request.POST
    
    search_text = request.POST.get('searchtext')

    
    # ----------------- Filter the articles ------------------  
    if "all" in form :
        entries = Entry.objects.filter(profile = my_profile)
        
    if "published" in form :
        entries = Entry.objects.filter(profile = my_profile , uploaded = True )
        
    if "unpublished" in form :
        entries = Entry.objects.filter(profile = my_profile, uploaded = False ) 
        
    
    # ----------------- Sorting the articles ------------------    
     
    if "nameup" in form :
        entries = Entry.objects.filter(profile = my_profile).order_by("-entry_title")
        
    if "namedown" in form :
        entries = Entry.objects.filter(profile = my_profile).order_by("entry_title")
        
    if "dateup" in form :
        entries = Entry.objects.filter(profile = my_profile ).order_by("-date_added")
        
    if "datedown" in form :
        entries = Entry.objects.filter(profile = my_profile).order_by("date_added") 
        
    # ----------------- Searching the articles ------------------ 
       
    if "searchtext" in form :
        entries = Entry.objects.filter(entry_title__contains = search_text ).order_by("-date_added") 
        
    context = {  "entries":entries , }
    return render(request,"blogyapp/articles.html" , context)

def publish_or_unpublish(request , entry_id):
    entry = Entry.objects.get(id = entry_id)
    uploaded = entry.uploaded
    profile_for_article = Profile.objects.get(name = request.user )
    
 
    entries = Entry.objects.filter(profile = profile_for_article) .order_by('-date_added') 
  
    if uploaded is True:
        uploaded = False
        entry.uploaded = uploaded
        entry.save(update_fields=['uploaded'])
        entry.save()
   
        return redirect("blogyapp:user_entries" )
        
    if uploaded is False:
        uploaded = True
        entry.uploaded = uploaded
        entry.save(update_fields=['uploaded'])
        entry.save()
      
        return redirect("blogyapp:user_entries" )
    
    
    return render(request, 'blogyapp/articles.html', {"entries":entries})
        
      
def dashboard(request):
    
    profile =Profile.objects.get(name = request.user ) #Profile of a specific user
    my_profile =Profile.objects.get(name =request.user)
    entries = Entry.objects.filter(profile = my_profile ).order_by("-date_added")
    profile_posts = profile.profiles_posts()
    profile_comments = Comments.objects.filter(profile = profile).order_by("-date_created")
    my_profile = Profile.objects.get(name =request.user)  
    followings = my_profile.following.all()  # people that the logged in user follows
    
    likes =  0
    bookmarks = 0
    
    for i in entries :
        likes = likes + i.likes
        
    for i in entries:
        bookmarks = bookmarks + i.bookmarks

    context ={"profile":profile,
              "followings":followings,
              "profile_posts":profile_posts,
             "profile_comments":profile_comments,
             "entries":entries,
             "likes":likes,
             "bookmarks":bookmarks ,
              }
    return render (request , "blogyapp/dashboard.html",context )


def notifications(request):

    my_profile =Profile.objects.get(name =request.user)  
    notifications = Notification.objects.filter( Q(entry__profile__name = request.user) | Q(profile__name = request.user) ).order_by("-date_created")
    

    followings = my_profile.following.all()
    my_guys = Profile.objects.filter(name__in = followings).exclude(Q(name=my_profile.name))[:6]  
    other_users = Profile.objects.exclude(name__in =followings).exclude(Q(name=my_profile.name))[:6] 
    
    
    context = { 
                "followings":followings, 
                "my_guys":my_guys ,
                "other_users":other_users , 
                "my_profile":my_profile,
                "notifications":notifications ,

                }
        
    
    return render (request , "blogyapp/notifications.html", context)