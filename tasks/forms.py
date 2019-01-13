from django.forms import ModelForm, CharField
from .models import Person

class RegistrationForm(ModelForm):
    secret = CharField(max_length=256)

    class Meta:
        model = Person
        fields = [ 'name', 'email', 'phone', 'tags' ]
