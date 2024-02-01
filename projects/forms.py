from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model=Project
        fields=['title','description','featured_image','demo_link','source_link','vote_total','vote_ratio','tags']
    
        widgets={
            'tags' : forms.CheckboxSelectMultiple()
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review
        fields=['value','body']
    
        labels={
            'value':'Place Your Vote',
            'body':'Add a Comment with your vote'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name , field in self.fields.items():
            field.widget.attrs.update({'class':'input'})