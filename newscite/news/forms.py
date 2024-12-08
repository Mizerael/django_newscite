from django import forms
from .models import Comment, News


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Ваш коментарий"}
            )
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ["title", "content", "image"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }
