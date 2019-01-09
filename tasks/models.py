from django.db import models
from django.core.validators import MinLengthValidator
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext as _
import uuid

class Event(models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, validators=[MinLengthValidator(3)])
    url = models.URLField(blank=True)
    description = models.TextField(verbose_name=_('Description'), blank=True)
    email = models.EmailField(verbose_name=_('Event organizer e-mail'), blank=True)
    active = models.BooleanField(verbose_name=_('Active'), default=False, help_text=_("Set to true to allow registration"))
    secret_question = models.CharField(verbose_name=_('Secret question'), blank=True, max_length=512, help_text=_("Question to ask for registration"))
    secret_answer = models.CharField(verbose_name=_('Secret answer'), blank=True, max_length=512, help_text=_("Answer to secret question"))
    public_tasks = models.BooleanField(verbose_name=_('Public tasks'), default=True, help_text=_("Show tasks in public views"))
    ask_email = models.BooleanField(verbose_name=_('Ask e-mail'), default=False, help_text=_("Ask email address in registration"))
    ask_phone = models.BooleanField(verbose_name=_('Ask phone'), default=False, help_text=_("Ask phone number in registration"))
    def __str__(self):
        return self.name
    class Meta:
       verbose_name = _('Event')
       verbose_name_plural = _('Events_')

class Tag(models.Model):
    event = models.ForeignKey(Event, verbose_name=_('Event'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(verbose_name=_('Description'), blank=True)
    def __str__(self):
        return self.event.name + "/" + self.name
    class Meta:
       verbose_name = _('Tag')
       verbose_name_plural = _('Tags_')

class Task(models.Model):
    event = models.ForeignKey(Event, verbose_name=_('Event'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=200, validators=[MinLengthValidator(3)])
    description = models.TextField(verbose_name=_('Description'), blank=True)
    points = models.IntegerField(verbose_name=_('Points'), default=100)
    min_assignees = models.PositiveIntegerField(verbose_name=_('Minimum assignees'), default=1, help_text=_("Minimum number of assignees for the task"))
    required_tags = models.ManyToManyField(Tag, verbose_name=_('Required tags'), blank=True, help_text=_("Tags required for task assignees"))

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def __str__(self):
        return self.event.name + "/" + self.name
    class Meta:
       verbose_name = _('Task')
       verbose_name_plural = _('Tasks_')

class Person(models.Model):
    event = models.ForeignKey(Event, verbose_name=_('Event'), on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=200, unique=True, validators=[MinLengthValidator(3)])
    email = models.EmailField(verbose_name=_('E-mail'), null=True, blank=True)
    phone = models.CharField(verbose_name=_('Phone'), max_length=100, null=True, blank=True)
    tags = models.ManyToManyField(Tag, verbose_name=_('Tags'), blank=True, help_text=_("Tags for this person"))
    modifycode = models.UUIDField(verbose_name=_('Modification code'), default=uuid.uuid4, editable=False)

    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }

    def __str__(self):
        return self.name
    class Meta:
       verbose_name = _('Person')
       verbose_name_plural = _('Persons_')

class Assignment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    @property
    def event(self):
        return self.task.event

    def __str__(self):
        return self.task.name + " -> " + self.person.name

    class Meta:
       verbose_name = _('Assignment')
       verbose_name_plural = _('Assignments_')
