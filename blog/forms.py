from django import forms
from .models import Post, Comment, ReplyToComment
from django.contrib import auth

class PostForm(forms.ModelForm):

  class Meta:
    model = Post
    fields = ('title', 'text',);

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)
        
class ContactForm(forms.Form):
    your_name = forms.CharField(max_length=50, required=True)
    your_email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=100, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class SearchForm(forms.Form):
    search_string = forms.CharField(max_length=200)

class ReplyToCommentForm(forms.ModelForm):

    class Meta:
        model = ReplyToComment
        fields = ('author', 'text',)