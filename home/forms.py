from django import forms
from home.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactModel
        fields = (
            'name' ,
            'email',
            'subject',
            'message'
        )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
        
            field.widget.attrs.update({'class': 'form-control'}),
            field.widget.attrs.update({'class': 'form-control'}),
            field.widget.attrs.update({'class': 'form-control'}),
            field.widget.attrs.update({'class': 'form-control'}),