
from django.shortcuts import render, redirect

from django.contrib.auth.models import User 
from .models import Topic, Entry , Comments

from django.contrib.admin.models import LogEntry 
from .forms import TopicForm, EntryForm , CommentsForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

from users.models import Profile
from itertools import chain

from django.db.models import Q

# Create your views here.


def home1(request):
    popular = Entry.objects.order_by("-popularity")[:4]
    if request.user.is_authenticated:
        user = request.user
        my_profile =Profile.objects.get(name =request.user)  # profile of logged in user
        
        entries = []
        sorted_articles = None
        
        
        followings = my_profile.following.all()#queryset of all the accounts that i follow ...
        my_guys = Profile.objects.filter(name__in = followings)[:4]  
        other_users = Profile.objects.exclude(name__in =followings)[:4]  
        profiles = [name for name in followings]
        
        for i in profiles:
            p = Profile.objects.get(name=i)
            p_posts = p.entry_set.all()
            entries.append(p_posts)
            
        my_posts = my_profile.profiles_posts()
        entries.append(my_posts)    
        
        if len(entries)>0:
            sorted_articles = sorted(chain(*entries) , reverse = True , key = lambda obj: obj.date_added)
            
        
        context = { "entries":sorted_articles  , "followings":followings, "my_guys":my_guys ,"other_users":other_users , "user":user,
                   "my_profile":my_profile }
        return render(request, 'blogyapp/home1.html',context)
    
    
    else:
    
        return render(request, 'blogyapp/home1.html' , {"popular":popular})


  
@login_required
def index(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')  # all topics of the current logged in user
    k = []
    for i in topics:
        
        x = i.entry_set.all()
        k.append(x)

    context = {'topics': topics,"k":k}
    return render(request, 'blogyapp/home.html', context )

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added') 
    if request.method == 'POST':
        if 'unpublished' in request.POST:
            entries = topic.entry_set.filter(uploaded=False).order_by('-date_added')  # unpublished
            context = {'topic': topic, 'entries': entries}
            return render(request, 'blogyapp/topics.html', context)
            
            
        if 'published' in request.POST:
            entries = topic.entry_set.filter(uploaded=True).order_by('-date_added')   # published
            context = {'topic': topic, 'entries': entries}
            return render(request, 'blogyapp/topics.html', context) 
        
        
        # Sorting the articles  
        
        if 'namedown' in request.POST:
            entries = topic.entry_set.order_by('entry_title')  # unpublished
            context = {'topic': topic, 'entries': entries}
            return render(request, 'blogyapp/topics.html', context)
            
            
        if 'nameup' in request.POST:
            entries = topic.entry_set.order_by('-entry_title')   # published
            context = {'topic': topic, 'entries': entries}
            return render(request, 'blogyapp/topics.html', context) 
        
        if 'datedown' in request.POST:
            entries = topic.entry_set.order_by('date_added')  # unpublished
            context = {'topic': topic, 'entries': entries}
            return render(request, 'blogyapp/topics.html', context)
            
            
        if 'dateup' in request.POST:
            entries = topic.entry_set.order_by('-date_added')   # published
            context = {'topic': topic, 'entries': entries}
            return render(request, 'blogyapp/topics.html', context) 
        
        
        # searching
        
        if 'search' in request.POST:
            search = request.POST.get('searchtext')
            
            print(search)
            entries = topic.entry_set.filter(Q(entry_title__icontains = search) | Q( introduction__icontains=search ) | Q(text__icontains = search) ).order_by('-date_added')   # published
            context = {'topic': topic, 'entries': entries}
            return render(request, 'blogyapp/topics.html', context) 
    
    
    return render(request, 'blogyapp/topics.html', {"topic":topic,"entries":entries})
        
        
        
    

@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            form.save()
            get_id = form.instance.id
            print(get_id)
            # should this have an id??
            return redirect('blogyapp:topic', topic_id=get_id)
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogyapp/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    profile = Profile.objects.get(name =request.user)  # current logged in user profile

    if request.method != 'POST':
        form = EntryForm()
    else:  # the form is  submited
        form = EntryForm(request.POST , request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.profile = profile
            new_entry.save()
            get_id = form.instance.id   # here we are getting the unique id of a specific entry !!
            print(get_id)
            # this summon all the entrie from all the topics !!
            entry = Entry.objects.get(id=get_id)
            if 'upload' in request.POST:

                entry.uploaded = True  # please note
                entry.save(update_fields=['uploaded'])

            # WHAT IN THE WORLD IS GOING ON HERE!!!
            return redirect('blogyapp:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'blogyapp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    # whats this topic : he is fetching the foreign key...getting access to all the Topic fields
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogyapp:topic',  topic_id=topic.id)

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'blogyapp/edit_entry.html', context)

@login_required
def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    # if topic.owner != request.user:
   #     raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry.
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            # should return to itself after clicking the updated form ** the initial link
            return redirect('blogyapp:index')

    context = {'topic': topic, 'form': form}
    return render(request, 'blogyapp/edit_topic.html', context)


@login_required
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    entry.delete()
    return redirect('blogyapp:topic', topic_id=topic.id)

@login_required
def delete_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    topic.delete()
    return redirect('blogyapp:index')

@login_required
def dashboard(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
  
    recent_5 =[]
    entry = Entry.objects.filter(topic__owner=request.user)
    for i in entry:
        recent_5.append(i)

   
    uploaded_entries = []
    draft_entries = []
    for i in entry:
        if i.uploaded is True:
            uploaded_entries.append(i)
        else:
            draft_entries.append(i)

    context = {'topics': topics, "entry": entry, "uploaded_entries": uploaded_entries,
               "draft_entries": draft_entries,  "recent_5":recent_5}
    return render(request, 'blogyapp/dashboard.html', context)

@login_required
def upload(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            topic.save(update_fields=['uploaded'])
            topic.uploaded = True  # please note
            new_entry.save()
            topic.save(update_fields=['uploaded'])
            # WHAT IN THE WORLD IS GOING ON HERE!!!
            return redirect('blogyapp:topic', topic_id=topic_id)
    context = {'topic': topic, 'form': form}
    return render(request, 'blogyapp/new_entry.html', context)


def read(request, read_id):
    my_profile = Profile.objects.get(name =request.user)  
    followings = my_profile.following.all()
    entry = Entry.objects.get(id=read_id) 
    comments = Comments.objects.filter( entry = entry)  # showing only the comments of a specific entry post
    topic = entry.topic
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
    
    context = {"entry": entry, "form":form , "topic":topic ,"comments":comments , "followings":followings}
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
    
    entry = Entry.objects.get(id = entry_id)
    profile = Profile.objects.get(name = request.user)
    liked_articles = profile.liked_articles.all()
    
    number_of_likes = entry.likes
    
    popularity = entry.popularity
    
    print(number_of_likes)
    
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
        
        return redirect('blogyapp:read', entry_id )

def bookmark(request,entry_id):
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
            
        
        return redirect('blogyapp:read', entry_id )
    
def my_bookmarks(request, profile_id):
    
    return render(request,"blogyapp/bookmarks.html")

def user_entries(request):
    
    return render(request,"blogyapp/user_entries.html")

def publish_or_unpublish(request , entry_id):
    entry = Entry.objects.get(id = entry_id)
    
    topic = entry.topic
    
    topics = Topic.objects.get(id=topic.id)
    
    entries = topic.entry_set.order_by('-date_added') 
    uploaded = entry.uploaded
    print(uploaded)
    
    if uploaded is True:
        uploaded = False
        entry.uploaded = uploaded
        entry.save(update_fields=['uploaded'])
        entry.save()
        topic.save()
        return redirect("blogyapp:topic",topic.id )
        
    if uploaded is False:
        uploaded = True
        entry.uploaded = uploaded
        entry.save(update_fields=['uploaded'])
        entry.save()
        topic.save()
        return redirect("blogyapp:topic",topic.id )
    
    
    return render(request, 'blogyapp/topics.html', {"topic":topics,"entries":entries})
        
    


        
    
    
