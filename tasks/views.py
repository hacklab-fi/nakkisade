from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils.translation import gettext as _
from django.db.models import Count
from django.conf import settings
from .models import Event, Person, Task, Assignment
from .forms import RegistrationForm
from operator import attrgetter
from django.core.mail import send_mail

def index(request):
    event_list = Event.objects.filter(active=True)
    context = {'event_list': event_list}
    return render(request, 'tasks/index.html', context)

def event(request, event_id):
    return render(request, 'tasks/event.html', {'event': check_event(event_id)})

def modify_registration(request, event_id, modifycode):
    event = check_event(event_id)

    person = None
    selected_tags = set()

    # If there's a modifycode, read the existing tags
    if modifycode:
        person = get_object_or_404(Person, modifycode=modifycode)
        for tag in person.tags.all():
            selected_tags.add(tag.id)

    if request.method == 'POST':
        form = RegistrationForm(request.POST, instance = person)

        if event.secret_question:
            secret = form.secret
            if secret != event.secret_answer.lower():
                form.add_error('secret', _("Wrong answer to secret question!"))

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email'] if event.ask_email else None
            phone = form.cleaned_data['phone'] if event.ask_phone else None
            if modifycode:
                person = get_object_or_404(Person, modifycode = modifycode)
                person.name = name
                person.email = email
                person.phone = phone
            else:
                person = Person(name = name, email = email, phone=phone, event = event)
            person.full_clean()
            for tag in request.POST.getlist('tag'):
                selected_tags.add(int(tag))
            person.save()
            # Clear tags & rebuild the list from what's posted
            person.tags.set([])
            for tag in event.tag_set.all():
                if str(tag.id) in selected_tags:
                    person.tags.add(tag)
            person.save()
            # No modifycode = registering for first time
            if not modifycode:
                modifycode = person.modifycode
                modifylink = modify_link_for(person, event, request)
                send_registration_mail(event, person, modifylink)
                return render(request, 'tasks/thanks.html', { 'event': event, 'modifylink': modifylink })
    else:
        form = RegistrationForm()
        if modifycode:
            form = RegistrationForm(instance=person)
            
    return render(request, 'tasks/register.html', { 'event': event, 'form': form, 'tags': selected_tags, 'modifycode': modifycode })

def send_registration_mail(event, person, modifylink):
    if not settings.EMAIL_HOST:
        print('No e-mail host set, not sending mail.')
        return
    send_mail(
        _('Registration to %(eventname)s') % { 'eventname': event.name },
        _('You have registered to this event via Nakkisade.') + '\n\n' +
        _('Use this link to modify your information:') + ' ' + modifylink,
        event.email if event.email else 'nakkisade@nakkisade.invalid',
        [ person.email ],
        fail_silently=True
    )

def register(request, event_id):
    return modify_registration(request, event_id, None)

def check_secret(request, event_id):
    event = check_event(event_id)
    if event.secret_question:
        secret = request.POST['secret'].strip().lower()
        if secret != event.secret_answer.lower():
            return "False"
    return "True"

def addperson(request, event_id):
    return render(request, 'tasks/thanks.html', { 'modifycode': modifycode })

# Returns event for given id if it exists and is active
def check_event(event_id):
    try:
        event = Event.objects.get(pk=event_id)
        if not event.active:
            raise Http404(_("Event not active"))
        return event
    except Event.DoesNotExist:
        raise Http404(_("Event does not exist"))

def tasklist(request, event_id):
    event = check_event(event_id)
    if not request.user.is_authenticated:
        return render(request, 'tasks/event.html', {'event': event, 'error_message': _("Must be logged in for this operation!")})
    tasks = Task.objects.filter(event=event)
    persons = Person.objects.filter(event=event)

    for person in persons:
        person.task_points = task_points_for(person)
        person.assignments = Assignment.objects.filter(person=person)

    for task in tasks:
        task.assigned = assignments_for(task)
        task.complete = len(task.assigned) >= task.min_assignees # True if task has enough people or has failed

    return render(request, 'tasks/tasklist.html', {'event': event, 'tasks': tasks, 'persons': persons})

def task_points_for(person):
    assignments = Assignment.objects.filter(person=person)
    task_points = 0
    for assignment in assignments:
        task_points = task_points + assignment.task.points
    return task_points

def assignments_for(task):
    assigned = []
    assignments = Assignment.objects.filter(task=task)
    for assignment in assignments:
        assigned.append(assignment.person)
    return assigned

def list_persons_available_for(task, persons):
    shortlist = []
    for person in persons:
        person_valid = True

        # Check if person has all required tags
        for tag in task.required_tags.all():
            if not tag in person.tags.all():
                person_valid = False

        # Check if person already has this task
        if Assignment.objects.filter(person=person,task=task).exists():
            person_valid = False

        if person_valid:
            shortlist.append(person)
    return shortlist

def create_tasks(request, event_id):
    event = check_event(event_id)
    if not request.user.is_authenticated:
        return render(request, 'tasks/event.html', {'event': event, 'error_message': _("Must be logged in for this operation!")})
    tasks = Task.objects.filter(event=event).annotate(num_tags=Count('required_tags')).order_by('-num_tags')
    persons = Person.objects.filter(event=event)
    if len(persons) == 0:
        return render(request, 'tasks/event.html', {'event': event, 'error_message': _("Must have at least one person!")})
    if len(tasks) == 0:
        return render(request, 'tasks/event.html', {'event': event, 'error_message': _("Must have at least one task!")})

    # Clear assignments
    # Assignment.objects.filter(task__event=event).delete()

    # Init some variables to work with
    for person in persons:
        person.task_points = task_points_for(person)

    for task in tasks:
        task.assigned = assignments_for(task)
        task.complete = len(task.assigned) >= task.min_assignees # True if task has enough people or has failed
        task.failed = False # True if couldn't find enough people

    # Changes to true when all tasks have been assigned (or failed to do so)
    all_assigned = False

    while not all_assigned:
        all_assigned = True
        for task in tasks:
            if not task.complete:
                assigned = None
                shortlist = list_persons_available_for(task, persons)
                shortlist = sorted(shortlist, key=attrgetter('task_points'))
                if len(shortlist) > 0:
                    assigned = shortlist[0]
                if assigned:
                    assignment = Assignment(task = task, person = assigned)
                    assignment.save()
                    assigned.task_points = assigned.task_points + task.points
                    task.assigned.append(assigned)

                    if len(task.assigned) >= task.min_assignees:
                        task.complete = True
                    else:
                        all_assigned = False
                else:
                    task.failed = True
                    task.complete = True
    return tasklist(request, event_id)

def modify_link_for(person, event, request):
    if hasattr(settings, 'URL_PREFIX'):
        return settings.URL_PREFIX + reverse('tasks:modify_registration', kwargs={'event_id': event.id, 'modifycode': person.modifycode })
    return request.build_absolute_uri(reverse('tasks:modify_registration', kwargs={'event_id': event.id, 'modifycode': person.modifycode }))
