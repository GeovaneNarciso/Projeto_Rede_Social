from django import forms
from postagem.models import Post


class FormPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['id', 'texto', 'foto']

    def __init__(self, *args, **kwargs):
        super(FormPost, self).__init__(*args, **kwargs)
        self.fields['foto'].required = False
