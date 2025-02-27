from django import forms
from .models import CustomUser


class Forgot_password_form(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Munday email adres yoq ")
        return email
