from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
    max_length=150,
    widget=forms.TextInput(attrs={'placeholder': 'Tu nombre de usuario', 'class':'main__input'}))
        
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder':'Tu contraseña', 'class':'main__input'})
    )

User = get_user_model()

class RegisterForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Define tu nombre de usuario', 'class':'main__input'})
    )

    email = forms.EmailField(
        label="Correo Electronico",
        widget=forms.EmailInput(attrs={'placeholder': 'tu@gmail.com', 'class':'main__input'})
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Introduce tu contraseña', 'class':'main__input'})
    )
    password_confirm = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repite tu contraseña', 'class':'main__input'})
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya esta en uso.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este nombre de usuario ya esta en uso.")
        return email
    
    def clean(self):

        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password !=password_confirm:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data