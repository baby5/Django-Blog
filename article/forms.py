from django import forms
from .models import Article, ArticleComment


class ArticleCommentForm(forms.ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['user_name', 'user_email', 'content']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'placeholder': 'Username',
            }),
            'user_email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'content': forms.Textarea(attrs={
                'placeholder': 'do a little work~'
            }),
        }
