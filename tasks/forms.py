from django.forms import ModelForm
from .models import Person

class RegistrationForm(ModelForm):
    class Meta:
        model = Person
        fields = [ 'name', 'email', 'phone', 'tags' ]
