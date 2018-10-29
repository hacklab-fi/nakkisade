from django.db import models
from django.core.validators import MinLengthValidator
from django.forms import CheckboxSelectMultiple

class Event(models.Model):
    name = models.CharField(max_length=200, unique=True, validators=[MinLengthValidator(3)])
    url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False, help_text="Set to true to allow registration")
    secret_question = models.TextField(blank=True, help_text="Question to ask for registration")
    secret_answer = models.TextField(blank=True, help_text="Answer to secret question")
    public_tasks = models.BooleanField(default=True, help_text="Show tasks in public views")
    ask_email = models.BooleanField(default=False, help_text="Ask email address in registration")
    ask_phone = models.BooleanField(default=False, help_text="Ask phone number in registration")
    def __str__(self):
        return self.name

class Tag(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True)
    def __str__(self):
        return self.event.name + "/" + self.name

class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True)
    min_assignees = models.PositiveIntegerField(default=1, help_text="Minimum number of assignees for the task")
    required_tags = models.ManyToManyField(Tag, blank=True, help_text="Tags required for task assignees")

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def __str__(self):
        return self.event.name + "/" + self.name

class Person(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, validators=[MinLengthValidator(3)])
    email = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, help_text="Tags for this person")

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def __str__(self):
        return self.name
