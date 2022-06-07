from django.shortcuts import render, redirect

from django.contrib.auth.models import User 
from .models import Topic, Entry

from django.contrib.admin.models import LogEntry , ADDITION
from .forms import TopicForm, EntryForm

from django.contrib.auth.decorators import login_required
from django.http import Http404

from PIL import Image

# Create your views here.


def home1(request):
    entry = Entry.objects.filter(topic__owner=request.user)[0:3]  # getting data from the Entry MOdel....

    context = {"entry": entry}
    return render(request, 'blogyapp/home1.html',context)
@login_required
def index(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
    #topics = Topic.objects.order_by('date_added')
    return render(request, 'blogyapp/home.html', {'topics': topics})
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    #topic = Topic.objects.filter(owner=request.user).order_by('date_added')
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

    if request.method != 'POST':
        form = EntryForm()
    else:  # the form is  submited
        form = EntryForm(request.POST , request.FILES)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
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

def dashboard(request):
    topics = Topic.objects.filter(owner=request.user).order_by('-date_added')
  
    recent_5 =[]
    entry = Entry.objects.filter(topic__owner=request.user)
    for i in entry:
        recent_5.append(i)
        

    
    activity = LogEntry.objects.filter(action_flag = ADDITION)
    uploaded_entries = []
    draft_entries = []
    for i in entry:
        if i.uploaded is True:
            uploaded_entries.append(i)
        else:
            draft_entries.append(i)

    context = {'topics': topics, "entry": entry, "uploaded_entries": uploaded_entries,
               "draft_entries": draft_entries, "activity": activity , "recent_5":recent_5}
    return render(request, 'blogyapp/dashboard.html', context)

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
    entry = Entry.objects.get(id=read_id)  # getting data from the Entry MOdel....
    topic = entry.topic  # summoned the foreignkey...now i have access to all fields of the Topic Model
    context = {"entry": entry, "topic":topic}
    return render(request, "blogyapp/read.html", context)

def practice(request):
    
    return render(request , "blogyapp/practice.html")
