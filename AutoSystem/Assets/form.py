from django import forms
from django.forms import ModelForm,TextInput,SelectMultiple,Select
from Assets.models import *
from django.db import models

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    #host_name = forms.CharField(attrs={'size': 10, 'title': 'Your name',})
    host_nip = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
class HostsFrom(ModelForm):
    class Meta:
        model = Host
        fields = ['host_name','host_nip','area','group']
        widgets = {
            'host_name': TextInput(attrs={'class': 'form-control'}),
            'host_nip': TextInput(attrs={'class': 'form-control'}),
            'area': Select(attrs={'class': 'form-control'}),
            'group': Select(attrs={'class': 'form-control'}),

        }

class AddBranchFrom(forms.Form):
    branch_name = forms.CharField(widget=forms.TextInput(attrs={'size': 10, 'title': 'Your name','class': 'form-control'}), label='Branch Name')
    Create_from = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }), help_text='Existing branch name, tag, or commit SHA')

class AddTagFrom(forms.Form):
    error_css_class = 'error'
    required_css_class = 'required'
    tag_name = forms.CharField(widget=forms.TextInput(attrs={'size': 10, 'title': 'Your name','class': 'form-control'}),label='Tag Name')
    Create_from = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control' }))

class ContactForm(forms.Form):
    host_name = forms.CharField(max_length=100)
    host_nip = forms.CharField(widget=forms.Textarea)
    area = forms.EmailField()
    group = forms.BooleanField(required=False)