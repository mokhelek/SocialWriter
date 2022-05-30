
from django import forms 
from .models import Topic , Entry
from tinymce.widgets import TinyMCE
class TopicForm(forms.ModelForm):
    text = forms.CharField(widget= forms.Textarea(attrs={'cols': 10, 'rows':2}))
    topic_description = forms.CharField(widget= forms.Textarea(attrs={'cols': 20, 'rows':2}))
    class Meta:
        model = Topic
        fields = ['text','topic_description']
        labels = {'text': 'topic_description'}

class EntryForm(forms.ModelForm):
    thumbnail = forms.ImageField()
    introduction = forms.CharField(widget= forms.Textarea())
    entry_title = forms.CharField(widget = forms.Textarea(attrs={'cols': 10, 'rows':1}))
    text = forms.CharField(widget = TinyMCE(attrs={'cols': 80, 'rows':20}))
    
    class Meta:
        model = Entry
        fields =['thumbnail' ,'entry_title','introduction','text']
        
        labels = {'text': 'Entry:'}
        #widgets = {'text': forms.Textarea(attrs={'cols': 80})}