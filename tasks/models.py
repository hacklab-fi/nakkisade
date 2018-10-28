from django.db import models
from django.core.validators import MinLengthValidator
from django.forms import CheckboxSelectMultiple

class Event(models.Model):
    name = models.CharField(max_length=200, unique=True, validators=[MinLengthValidator(3)])
    url = models.URLField(blank=True)
    active = models.BooleanField(default=False, help_text="Set to true to allow registration")
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
    tags = models.ManyToManyField(Tag, blank=True, help_text="Tags for this person")

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def __str__(self):
        return self.name
