from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.db.models import Count
from .models import Event, Person, Task
from operator import attrgetter

def index(request):
    event_list = Event.objects.filter(active=True)
    context = {'event_list': event_list}
    return render(request, 'tasks/index.html', context)

def event(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    if not event.active:
        raise Http404("Event does not exist")
    return render(request, 'tasks/event.html', {'event': event})

def register(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    if not event.active:
        raise Http404("Event does not exist")
    return render(request, 'tasks/register.html', {'event': event})

def addperson(request, event_id):
    name = request.POST['name']
    event = Event.objects.get(pk=event_id)
    if not event.active:
        raise Http404("Event not active")
    person = Person(name = name, event = event)
    person.full_clean()
    selected_tags = request.POST.getlist('tag')
    person.save()
    for tag in event.tag_set.all():
        if str(tag.id) in selected_tags:
            person.tags.add(tag)
    person.save()
    return render(request, 'tasks/thanks.html')

# The magic happens here
def find_person_for_task(event, persons, task):
    # Sort persons by task count
    sortedlist = sorted(persons, key=attrgetter('task_count'))
    assignee = None
    for person in sortedlist:
        person_valid = True
        # Check if person already has this task
        if task in person.tasks:
            break
        # Check if person has all required tags
        for tag in task.required_tags.all():
            if not tag in person.tags.all():
                person_valid = False
        if person_valid:
            assignee = person
            break

    return assignee

def tasklist(request, event_id):
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        raise Http404("Event does not exist")
    if not event.active:
        raise Http404("Event not active")
    if not request.user.is_authenticated:
        return render(request, 'tasks/event.html', {'event': event, 'error_message': "Must be logged in to get task list!"})
    tasks = Task.objects.filter(event=event).annotate(num_tags=Count('required_tags')).order_by('-num_tags')
    persons = Person.objects.filter(event=event)
    if len(persons) == 0:
        return render(request, 'tasks/event.html', {'event': event, 'error_message': "Must have at least one person!"})
    if len(tasks) == 0:
        return render(request, 'tasks/event.html', {'event': event, 'error_message': "Must have at least one task!"})

    # Init some variables to work with
    for person in persons:
        person.task_count = 0
        person.tasks = []

    for task in tasks:
        task.assigned = []
        task.complete = False # True if task has enough people or has failed
        task.failed = False # True if couldn't find enough people

    # Changes to true when all tasks have been assigned (or failed to do so)
    all_assigned = False

    while not all_assigned:
        all_assigned = True
        for task in tasks:
            if not task.complete:
                assigned = find_person_for_task(event, persons, task)
                if assigned:
                    assigned.task_count = assigned.task_count + 1
                    task.assigned.append(assigned)
                    assigned.tasks.append(task)
                    if len(task.assigned) >= task.min_assignees:
                        task.complete = True
                    else:
                        all_assigned = False
                else:
                    task.failed = True
                    task.complete = True

    return render(request, 'tasks/tasklist.html', {'event': event, 'tasks': tasks, 'persons': persons})
