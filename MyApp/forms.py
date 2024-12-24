from django import forms
from .models import Post,Profile

class NewPostform(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(required=True,widget=forms.TextInput(attrs={
            'placeholder': 'Enter Caption'
        }))
    tags = forms.CharField(required=True,widget=forms.TextInput(attrs={
            'placeholder': 'Enter Tags separated by comma'
        }))

    class Meta:
        model = Post
        fields = ['picture','caption','tags']

class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'User Name'}), required=True)
    profile_pic = forms.ImageField(required=True)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Bio'}), required=True)
    skills = forms.CharField(widget=forms.TextInput(attrs={'class': 'box', 'placeholder': 'Skills'}), required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'profile_pic', 'bio','skills']