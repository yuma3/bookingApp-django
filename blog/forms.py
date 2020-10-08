from django import forms
from .models import Tag, Comment, Reply
from .widgets import CustomCheckboxSelectMultiple
from .fields import SimpleCaptchaField


class PostSearchForm(forms.Form):

    key_word = forms.CharField(
        label='検索キーワード',
        required=False
    )
    tags = forms.ModelMultipleChoiceField(
        label='タグでの絞り込み',
        required=False,
        queryset=Tag.objects.order_by('name'),
        widget=CustomCheckboxSelectMultiple,
    )


class CommentCreateForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ('target', 'created_at')
        widgets = {
            'text' : forms.Textarea(
                attrs={
                    'placeholder': 'マークダウンに対応しています。'
                }
            )
        }
        captcha = SimpleCaptchaField()


class ReplyCreateForm(forms.ModelForm):

    class Meta:
        model = Reply
        exclude = ('target', 'created_at')
        widgets = {
            'text': forms.Textarea(
                attrs={'placeholder': 'マークダウンに対応しています。'}
            )
        }
        captcha = SimpleCaptchaField()
