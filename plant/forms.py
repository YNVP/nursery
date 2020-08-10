from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Plant
from nursery.models import Nursery


class PlantCreateForm(forms.ModelForm):

    class Meta:
        model = Plant
        fields = ['name', 'description', 'price', 'nursery', 'stock']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user)
        super(PlantCreateForm, self).__init__(*args, **kwargs)
        self.fields['nursery'].queryset = Nursery.objects.filter(user=user)
