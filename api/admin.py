from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import User, Role, Permission, Employee
from django.contrib.auth.models import Group


class UserCreationForm(forms.ModelForm):
    """
    A form for creating a new user from the admin panel.
    """

    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    validation_password = forms.CharField(
        label="Password Confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_password_validation(self):
        # Check if the given password match
        original = self.cleaned_data.get("password")
        verification = self.cleaned_data.get("validation_password")
        if original and verification and original != verification:
            raise ValidationError("Password don't match")
        return verification

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(Employee)
admin.site.unregister(Group)
