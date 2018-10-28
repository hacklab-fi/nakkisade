from django.db import models
from django.core.validators import MinLengthValidator
from django.forms import CheckboxSelectMultiple

class Event(models.Model):
    name = models.CharField(max_length=200, unique=True, validators=[MinLengthValidator(3)])
    url = models.URLField(blank=True)
    def __str__(self):
        return self.name

class Tag(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    def __str__(self):
        return self.event.name + "/" + self.name

class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(blank=True)
    min_assignees = models.PositiveIntegerField(default=1)
    required_tags = models.ManyToManyField(Tag, blank=True)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def __str__(self):
        return self.event.name + "/" + self.name

class Person(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True, validators=[MinLengthValidator(3)])
    tags = models.ManyToManyField(Tag, blank=True)
    assigned_tasks = models.ManyToManyField(Task, blank=True)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def __str__(self):
        return self.name
