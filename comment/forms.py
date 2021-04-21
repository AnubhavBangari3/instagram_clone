from django import forms
from . models import *

class CommentForm(forms.ModelForm):
    body=forms.CharField(widget=forms.Textarea(attrs={'class':"input is-medium"}),required=True)
    class Meta:
        model=Comment
        fields=('body',)