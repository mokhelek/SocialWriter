from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic , Entry
from .forms import TopicForm , EntryForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

# Create your views here.
def home1(request):
    #topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    #topics = Topic.objects.order_by('date_added')
    return render(request, 'blogyapp/home1.html' )
@login_required
def index(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    #topics = Topic.objects.order_by('date_added')
    return render(request, 'blogyapp/home.html', {'topics':topics} )

@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    #topic = Topic.objects.filter(owner=request.user).order_by('date_added')
    if topic.owner != request.user:
        raise Http404
    
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries }
    return render(request,'blogyapp/topics.html', context)

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
            return redirect('blogyapp:topic',topic_id = get_id ) #should this have an id??
    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'blogyapp/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('blogyapp:topic', topic_id=topic_id)  #WHAT IN THE WORLD IS GOING ON HERE!!!
    context = {'topic': topic, 'form': form}
    return render(request, 'blogyapp/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic  #whats this topic
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

def edit_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    #if topic.owner != request.user:
   #     raise Http404
    
    if request.method != 'POST':
    # Initial request; pre-fill form with the current entry.
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogyapp:index')  #should return to itself after clicking the updated form ** the initial link
            
    context = { 'topic': topic, 'form': form}
    return render(request, 'blogyapp/edit_topic.html', context)




def read(request , read_id):
    entry = Entry.objects.get(id=read_id)
    context = {"entry":entry}
    return render(request , "blogyapp/read.html", context)
@login_required
def delete_entry(request , entry_id ):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    entry.delete()

    return redirect('blogyapp:topic', topic_id =topic.id )
@login_required
def delete_topic(request, topic_id ):
    topic = Topic.objects.get(id=topic_id)
    topic.delete()
    return redirect('blogyapp:index')

def practice(request):


    return render(request, "blogyapp/practice.html")

    