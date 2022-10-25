from pyexpat import model
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .models import Profile


class UserRegistrationsForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields =['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image']