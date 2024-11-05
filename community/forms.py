from django import forms
from .models import Topic, TopicPost

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'description']

class TopicPostForm(forms.ModelForm):
    class Meta:
        model = TopicPost
        fields = ('description',)

        