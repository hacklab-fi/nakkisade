# Nakkisade

Event registration and task assigning tool

Status: beta

## What it does

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

## Running in Docker

The easiest way to run nakkisade is with docker. It takes admin credentials
as env variables:

```bash
docker image build . --name nakkisade
docker run -e ADMIN_USER=admin -e ADMIN_EMAIL=nakkisadeadmin@your.host -e ADMIN_PASSWORD=adminpassword  --name nakkisade -d nakkisade
```

If you use docker-compose, there's a file ready for you. Just modify the docker-environment.env file
for your needs.

## Running on host

Like any django app (example in Ubuntu 18.10)

```bash
pip3 install -r requirements.txt 
./manage.py makemigrations tasks
./manage.py migrate
./manage.py createsuperuser
django-admin compilemessages
./manage.py runserver
```

Use the admin interface to create events, tasks and tags.

URLs:

http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/tasks/

To generate task list, log in to app using the login link (use the admin account). 

## Custom settings

If you want custom settings, put them in settings_local.py. There's a template
version of it in nakkisade/. 

### Matrix support

Nakkisade supports notifications of registrations on a Matrix channel. Set the
relevant variables in settings_local.py (see template) and Nakkisade will
notify when people register on the notification channel.

## Developer stuff

To generate languages:

```bash
django-admin makemessages -l fi
django-admin compilemessages
```

## Credits

* Code & idea: Ville Ranki
* Logo: Manu Pärssinen
