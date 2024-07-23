# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.models import Group


class UserUpdateForm(UserChangeForm):
    """ Form to create new user """
    is_superuser = forms.BooleanField(
        label='Superuser status', required=False, initial=False)
    is_staff = forms.BooleanField(
        label='Staff status', required=False, initial=False)
    role = forms.CharField(max_length=50, required=True)

    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('username', 'cnie', 'role', 'is_superuser',
                  'is_staff', 'security_question', 'security_answer')

    def __init__(self, *args, **kwargs):
        # Extract instance and pass it to the form
        self.instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        # Remove username uniqueness check if instance is provided (i.e., for updates)
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
    """ Form to create new user """
    is_superuser = forms.BooleanField(
        label='Superuser status', required=False, initial=False)
    is_staff = forms.BooleanField(
        label='Staff status', required=False, initial=False)
    role = forms.CharField(max_length=50, required=True)
    security_question = forms.CharField(max_length=255, required=True)
    security_answer = forms.CharField(max_length=255, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'cnie', 'role', 'is_superuser',
                  'is_staff', 'security_question', 'security_answer')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = self.cleaned_data.get('is_superuser', False)
        user.is_staff = self.cleaned_data.get('is_staff', False)

        # Save the user instance to get an ID
        if commit:
            user.save()

        # Get or create the group based on the 'role' field
        role = self.cleaned_data.get('role')
        group, _ = Group.objects.get_or_create(name=role)

        # Add the user to the group
        user.groups.add(group)

        return user


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'cnie')
