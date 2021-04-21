
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=120, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=120, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class EditProfileForm(forms.ModelForm):
    picture=forms.ImageField(required=False)
    first_name = forms.CharField(widget=forms.TextInput(),max_length=120, required=False, )
    last_name = forms.CharField(widget=forms.TextInput(),max_length=120, required=False, )
    location=forms.CharField(widget=forms.TextInput(attrs={'class':"input is-medium"}),max_length=120,required=False)
    url=forms.CharField(widget=forms.TextInput(attrs={'class':"input is-medium"}),max_length=120,required=False)
    profile_info=forms.CharField(widget=forms.Textarea(attrs={'class':"input is-medium"}),max_length=120,required=False)
    class Meta:
        model=Profile
        fields=('picture','first_name','last_name','location','url','profile_info')
