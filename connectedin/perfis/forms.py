from django import forms
from perfis.models import *


class FormImage(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']

