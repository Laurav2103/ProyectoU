from pyexpat import model
from django import forms
from .models import article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = article
       # fields = '_all_'
        fields = ('nombreArticulo', 'segmento', 'categoria')
