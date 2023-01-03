

from django import forms 
from .models import Entry ,Comments
from tinymce.widgets import TinyMCE


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
        
class CommentsForm(forms.ModelForm):
    comment = forms.CharField(widget= forms.Textarea(attrs={'cols': 10, 'rows':3 , "placeholder":"Comments"}) , label="",)
    class Meta:
        model = Comments
        fields =["comment"]
        #label = {"comment":"Discussion"}