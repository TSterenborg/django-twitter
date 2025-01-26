from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, SetPasswordMixin

from .models import CustomUser
import re

class CustomUserCreationForm(UserCreationForm):
    display_name = forms.CharField(max_length=255)
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ('display_name', 'username', 'email', 'password1', 'password2')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^\w+$', username):
            raise ValidationError('Username mag alleen letters, cijfers en laagstreepjes (_) bevatten.')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('Deze username is al in gebruik.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Dit emailadres is al geregistreerd.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("De wachtwoorden komen niet overeen.")

        if password1:
            if len(password1) < 8:
                raise ValidationError("Het wachtwoord moet minstens 8 tekens bevatten.")
            common_passwords = ['123456', 'password', '123456789', 'qwerty', 'abc123', 'password1', '12345', '1234']
            if password1 in common_passwords:
                raise ValidationError("Het wachtwoord mag geen veelgebruikt wachtwoord zijn.")
            if password1.isdigit():
                raise ValidationError("Het wachtwoord mag niet volledig numeriek zijn.")
            if any(char.isdigit() for char in password1) and not any(char.isalpha() for char in password1):
                raise ValidationError("Het wachtwoord moet ten minste één letter bevatten.")
        return cleaned_data

class CustomUserEditForm(forms.Form):
    display_name = forms.CharField(label='display_name', max_length=255)
    email = forms.EmailField()
    password1, password2 = SetPasswordMixin.create_password_fields()

    def set_request(self, request):
        self.request = request

    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if CustomUser.objects.filter(email=email).exists() and email != self.request.user.email:
            raise ValidationError("Email bestaat al")
        
        common_passwords = ['123456', 'password', '123456789', 'qwerty', 'abc123', 'password1', '12345', '1234']

        if password1 and password2 and password1 != password2:
            raise ValidationError("De wachtwoorden komen niet overeen.")

        if password1:
            if len(password1) < 8:
                raise ValidationError("Het wachtwoord moet minstens 8 tekens bevatten.")
            common_passwords = ['123456', 'password', '123456789', 'qwerty', 'abc123', 'password1', '12345', '1234']
            if password1 in common_passwords:
                raise ValidationError("Het wachtwoord mag geen veelgebruikt wachtwoord zijn.")
            if password1.isdigit():
                raise ValidationError("Het wachtwoord mag niet volledig numeriek zijn.")
            if any(char.isdigit() for char in password1) and not any(char.isalpha() for char in password1):
                raise ValidationError("Het wachtwoord moet ten minste één letter bevatten.")

        return cleaned_data

    def save(self):
        
        user_model = CustomUser.objects.get(email=self.request.user.email)

        user_model.email = self.cleaned_data['email']
        user_model.display_name = self.cleaned_data['display_name']

        print(self.cleaned_data['password1'])

        if self.cleaned_data['password1'] != '':
            user_model.set_password(self.cleaned_data['password1'])

        print(user_model.email)

        user_model.save()