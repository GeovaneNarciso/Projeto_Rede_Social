from django import forms
from perfis.models import *


class FormFotoPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['foto']

