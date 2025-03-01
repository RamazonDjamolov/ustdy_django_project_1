from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import CustomUser, Code


class Forgot_password_form(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Munday email adres yoq ")
        return email


class RestorePasswordForm(forms.Form):
    username = forms.CharField(max_length=200)
    code = forms.CharField(max_length=4)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    re_password = forms.CharField(widget=forms  .PasswordInput(attrs={'class': 'form-control'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        code = self.cleaned_data.get('code')
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        user = CustomUser.objects.filter(username=username).first()

        if not user:
            raise ValidationError("username topilmadi")

        if not Code.objects.filter(user=user, code_number=code, expired_data__gt=timezone.now()):
            raise ValidationError(f"code topilmadi {timezone.now()}")

        if password != re_password:
            raise ValidationError("passwor most emas topilmadi")

        return self.cleaned_data

    def update(self):
        user = CustomUser.objects.filter(username=self.cleaned_data.get('username')).first()
        user.set_password(self.cleaned_data.get('password'))
        user.save()
