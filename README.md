# Nakkisade

Event registration and task assigning tool

Status: alpha

## What it does?

Nakkisade is intended for event organizers. Especially events in which volunteer
participants do some tasks such as hackathons, demoparties, underground raves, 
small festivals etc.

It does two things:

* Event registration for public
* Assigning task to registered people

As administrator you can create event(s) in it, and create tasks that need
to be done. You can also create tags for tasks such as "needs to be present on
saturday", "needs to use laptop", "carrying heavy stuff" etc.

Participants can register to the events, and specify what tags they have.

When administrator wants, nakkisade can generate a list of tasks and persons
who they are assigned. The tags are used to filter who can do what and tasks
are shared as evenly as possible.

In the end admin can print out a report of tasks and their assignees, and 
task lists for individuals.

## Running

Like any django app
```
./manage.py makemigrations tasks
./manage.py migrate
./manage.py createsuperuser
```

Use the admin interface to create events, tasks and tags.

URLs:

http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/tasks/

To generate task list, log in to app using the login link (use the admin account). 
