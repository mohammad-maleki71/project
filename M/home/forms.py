from django import forms
from .models import Post, Comment


class PostUpdateCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }

class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }