from django import forms
from postagem.models import Post


class FormPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['texto', 'foto']
