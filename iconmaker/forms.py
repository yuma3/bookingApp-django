
from django import forms
from .models import IconModel


class IconSearchForm(forms.Form):

    keyword = forms.CharField(label='キーワード', required=False)
