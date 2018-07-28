from django import forms
from pyuploadcare.dj.forms import FileWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Image, Profile, Comments

class ImageForm(forms.ModelForm):

    class Meta:
        model = Image
        exclude = ['likes', 'upload_date', 'user', 'name']
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['image', 'user']