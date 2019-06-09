from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

def index(request):
    '''Learning_logs aplication main page'''
    return render(request, 'learning_logs/index.html')

#@login_required
def topics(request):
    '''All topics'''
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

#@login_required
def topic(request, topic_id):
    """Show a single topic, and all its entries."""
    topic = Topic.objects.get(id=topic_id)

    entries = topic.entry_set.order_by('date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add new topic """
    if request.method != 'POST':
        #No info provided, create empty form
        form = TopicForm()
    else:
        #Data provided with POST
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    context = {'form': form}    
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Adding new entry to the topic"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        #No info added, creat empty form
        form = EntryForm()
    else:
        #Data provided with POST
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'topic': topic, 'form': form}    
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Editig existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        #No info added, create empty form
        form = EntryForm(instance=entry)
    else:
        #Data provided with POST
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic_id]))
    context = {'entry':entry, 'topic': topic, 'form': form}    
    return render(request, 'learning_logs/edit_entry.html', context)


























