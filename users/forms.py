
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text="")
    username = forms.CharField(widget=forms.TextInput , help_text = '')
    password1 = forms.CharField(widget=forms.TextInput , help_text = '')
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password1","password2")

