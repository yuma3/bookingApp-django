from django import forms


class SimpleCaptchaField(forms.CharField):

    def __init__(self, label='checker', **kwargs):
        super().__init__(label=label, required=True, **kwargs)
        self.widget.attrs['placeholder'] = '「メッシの背番号を書いてください。」'

    def clean(self, value):
        value = super().clean(value)
        if value == '10':
            return value
        else:
            raise forms.ValidationError('間違ってます。')
