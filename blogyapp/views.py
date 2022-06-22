from turtle import update
from django.shortcuts import render, redirect

from django.contrib.auth.models import User 
from .models import Topic, Entry , Comments

from django.contrib.admin.models import LogEntry 
from .forms import TopicForm, EntryForm , CommentsForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

from users.models import Profile

# Create your views here.


def home1(request):
    if request.user.is_authenticated:
        user = request.user
        my_profile =Profile.objects.get(name =request.user)  # profile of logged in user
        
        entries = []
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
        
        context = { "entries":entries , "followings":followings, "my_guys":my_guys ,"other_users":other_users , "user":user,
                   "my_profile":my_profile }
        return render(request, 'blogyapp/home1.html',context)
    else:
    
        return render(request, 'blogyapp/home1.html')


  
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
    
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'blogyapp/topics.html', context)

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
    entry = Entry.objects.get(id=read_id) 
    comments = Comments.objects.filter( entry = entry)  # showing only the comments of a specific entry post
    topic = entry.topic
    profile_login_user = Profile.objects.get(name = request.user)
    commenter = profile_login_user  #profile of logged in user
    
    if request.method != 'POST':
        form = CommentsForm()
    else:
        #profile = request.user  # variable has to be the actual database field
        form = CommentsForm(data=request.POST)
        if form.is_valid():
            form.profile_login_user = profile_login_user 
            new_comment = form.save(commit=False)
            new_comment.entry = entry 
            # first variable is the actual field from the model that you want to attach to ...
            # the second variable is the queryset or varible that you update with
            # in simple  terms this is a " from " & "to"
            new_comment.profile = commenter
            

            
            
            new_comment.save()
            return redirect('blogyapp:read', read_id= entry.id)
    
    context = {"entry": entry, "form":form , "topic":topic ,"comments":comments}
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
        
    if request.method == 'POST':
        return redirect('blogyapp:profile_detail', profile_id = profile.id)

    return render(request , "blogyapp/profile_detail.html" )
    
