# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group


class UserUpdateForm(UserChangeForm):
    """ Form to update user information """
    is_superuser = forms.BooleanField(
        label='Superuser status', required=False, initial=False)
    is_staff = forms.BooleanField(
        label='Staff status', required=False, initial=False)
    role = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'cnie', 'email', 'role', 'is_superuser',
                  'is_staff')

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['username'].required = False
            self.fields['username'].validators = []

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        user.is_staff = self.cleaned_data.get('is_staff', False)

        if commit:
            user.save()

        role = self.cleaned_data.get('role')
        if role:
            group, _ = Group.objects.get_or_create(name=role)
            user.groups.add(group)

        return user


class SignUpForm(UserCreationForm):
    """ Form to create a new user """
    email = forms.EmailField(required=True)
    is_superuser = forms.BooleanField(
        label='Superuser status', required=False, initial=False)
    is_staff = forms.BooleanField(
        label='Staff status', required=False, initial=False)
    role = forms.CharField(max_length=50, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'cnie', 'email', 'role', 'is_superuser',
                  'is_staff')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        user.is_staff = self.cleaned_data.get('is_staff', False)

        if commit:
            user.save()

        role = self.cleaned_data.get('role')
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'cnie')
