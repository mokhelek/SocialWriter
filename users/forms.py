from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(help_text="Required")
    
    class Meta:
        model = User
        fields = ("first_name","last_name","username","email","password1","password2")
    