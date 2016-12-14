from django import forms
from .models import Article, ArticleComment


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        models = ArticleComment
        fields = ['user_name', 'user_email', 'content']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'placeholder': 'Username',
            }),
            'user_email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'content': forms.TextInput(attrs={
                'placeholder': 'do a little work~'
            }),
        }
