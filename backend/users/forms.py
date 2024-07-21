# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class SignUpForm(UserCreationForm):
    is_superuser = forms.BooleanField(label='Superuser status', required=False)
    is_staff = forms.BooleanField(label='Staff status', required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'cnie', 'is_superuser', 'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = self.cleaned_data.get('is_superuser')
        user.is_staff = self.cleaned_data.get('is_staff')
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'cnie')
