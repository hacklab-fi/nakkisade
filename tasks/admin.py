from django.contrib import admin
from .models import Event, Person, Tag, Task

admin.site.register(Event)
admin.site.register(Person)
admin.site.register(Tag)
admin.site.register(Task)

