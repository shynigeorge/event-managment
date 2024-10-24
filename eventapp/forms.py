from django import forms
from .models import *

class eventForm(forms.ModelForm):
    class Meta:
        model = EventRegister
        exclude = ["status"]