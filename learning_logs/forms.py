from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):
    class meta:
        model = Topic
        fields = ['text']
        labels = {'text':''}