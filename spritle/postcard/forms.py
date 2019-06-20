from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', )



class PostcardForm(forms.Form):
    post = forms.CharField(label="Send a Postcard!", widget=forms.Textarea(attrs={"rows": 3, "cols": 100}))


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 3, "cols": 100}))



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].widget = forms.widgets.Textarea(attrs={"rows": 3, "cols": 100})
        
