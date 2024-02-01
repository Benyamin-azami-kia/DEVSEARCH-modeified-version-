from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password1','password2']

        error_messages={
			"first_name":{
				"required":"This Field Is Required"
			}
		}
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['profile_image','short_intro','bio','location','social_github'
                ,'social_twitter','social_linkedin','social_youtube'
                ,'social_website']
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class SkillForm(forms.ModelForm):
    class Meta:
        model=Skill
        fields=['name','description']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
    
    def save(self, request):
        skill= super().save(commit=False)
        skill.owner=request.user.profile
        skill.save()


class UserEditForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email']
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class MessageForm(forms.ModelForm):
    class Meta:
        model=Message
        fields=['subject','body']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})