from django.forms import ModelForm, CharField, Field
from .models import Person

class RegistrationForm(ModelForm):
    secret = CharField(max_length=256, required=False)

    class Meta:
        model = Person
        fields = [ 'name', 'email', 'phone', 'tags' ]
